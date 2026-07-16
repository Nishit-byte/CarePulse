import cv2
import mediapipe as mp
import numpy as np
import time
import os
import joblib
import pandas as pd
from dotenv import load_dotenv
from twilio.rest import Client
from pose_utils import extract_features
from database import init_db, get_live_person, log_alert, resolve_alert, set_person_status

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TWILIO_TO = os.getenv("TWILIO_WHATSAPP_TO")

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)

model = joblib.load("models/fall_classifier.pkl")

MOTIONLESS_SECONDS = 10
MOTIONLESS_DELTA = 0.015

def send_whatsapp_alert(location="Living Room"):
    if not all([TWILIO_SID, TWILIO_AUTH, TWILIO_FROM, TWILIO_TO]):
        print("WARNING: Twilio credentials missing in .env - skipping WhatsApp alert.")
        return None
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        timestamp = time.strftime("%I:%M %p")
        body = (
            f"Emergency Alert\n"
            f"A possible fall has been detected.\n"
            f"Time: {timestamp}\n"
            f"Location: {location}\n"
            f"Please check on the person immediately."
        )
        client.messages.create(body=body, from_=TWILIO_FROM, to=TWILIO_TO)
        print(f"WhatsApp alert sent successfully at {timestamp}.")
        return timestamp
    except Exception as e:
        print(f"ERROR sending WhatsApp alert: {e}")
        return None

def main():
    init_db()
    live_person = get_live_person()
    if live_person is None:
        print("No live person found. Run seed_data.py first.")
        return

    person_id = live_person["id"]
    device_id = live_person["device_id"]
    room = live_person["room"]
    print(f"Monitoring started for: {live_person['name']} ({room})")

    cap = cv2.VideoCapture(0)
    prev_hip_center = None
    fall_candidate_time = None
    motionless_start_time = None
    alert_sent = False
    current_alert_id = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Camera frame not received. Exiting.")
            break

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            features, hip_center = extract_features(landmarks, w, h, prev_hip_center)
            velocity = features["velocity"]
            prev_hip_center = hip_center

            X = pd.DataFrame([features])
            prediction = model.predict(X)[0]
            fall_prob = model.predict_proba(X)[0][1]

            if prediction == 1 and fall_candidate_time is None:
                fall_candidate_time = time.time()
                motionless_start_time = time.time()
                alert_sent = False
                print("Fall candidate detected. Starting 10s confirmation timer.")

            if fall_candidate_time is not None:
                if velocity < MOTIONLESS_DELTA:
                    elapsed = time.time() - motionless_start_time
                    if elapsed >= MOTIONLESS_SECONDS and not alert_sent:
                        print("Fall confirmed. Logging to database and attempting WhatsApp alert.")
                        try:
                            current_alert_id = log_alert(person_id, device_id, float(fall_prob), priority="High")
                            print(f"Alert logged to database with id {current_alert_id}.")
                        except Exception as e:
                            print(f"ERROR logging alert to database: {e}")
                        send_whatsapp_alert(location=room)
                        alert_sent = True
                    cv2.putText(frame, f"FALL DETECTED: {int(elapsed)}s", (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    fall_candidate_time = None
                    motionless_start_time = None
                    if alert_sent and current_alert_id:
                        try:
                            resolve_alert(current_alert_id, person_id)
                        except Exception as e:
                            print(f"ERROR resolving alert: {e}")
                        current_alert_id = None
                    alert_sent = False
                    try:
                        set_person_status(person_id, "All Good")
                    except Exception as e:
                        print(f"ERROR updating person status: {e}")
            else:
                try:
                    set_person_status(person_id, "All Good")
                except Exception as e:
                    print(f"ERROR updating person status: {e}")

        cv2.imshow("Fall Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()