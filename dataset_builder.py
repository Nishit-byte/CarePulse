import os
import cv2
import mediapipe as mp
import pandas as pd 
from pose_utils import extract_features


mp_pose = mp.solutions.pose

def parse_annotation(annotation_path):
    with open(annotation_path, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if "," in lines[0]:
        return -1, -1
    start_frame = int(lines[0])
    end_frame = int(lines[1])
    return start_frame, end_frame

def process_video(video_path, annotation_path, pose):
    start_frame, end_frame = parse_annotation(annotation_path)
    cap = cv2.VideoCapture(video_path)
    rows = []
    frame_idx = 0
    prev_hip_center = None

    while cap.isOpened():
        ret, frame  = cap.read()
        if not ret:
            break
        frame_idx += 1
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            features, hip_center = extract_features(landmarks, w, h, prev_hip_center)

            prev_hip_center = hip_center
            label = 1 if start_frame <= frame_idx <= end_frame else 0 
            features["label"] = label
            rows.append(features)

    cap.release()
    return rows

def build_dataset(dataset_root, output_csv):
    pose = mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)
    all_rows = []
    
    for subset in os.listdir(dataset_root):
        outer_path = os.path.join(dataset_root, subset)
        inner_path = os.path.join(outer_path, subset)
        subset_path = inner_path if os.path.isdir(inner_path) else outer_path
        annotations_dir = os.path.join(subset_path, "Annotation_files")
        videos_dir = os.path.join(subset_path, "Videos")
        

        if not os.path.isdir(videos_dir) or not os.path.isdir(annotations_dir):
            continue
        for video_file in os.listdir(videos_dir):
            name, ext = os.path.splitext(video_file)
            annotation_file = name + ".txt"
            annotation_path = os.path.join(annotations_dir, annotation_file)
            video_path = os.path.join(videos_dir, video_file)

            if not os.path.exists(annotation_path):
                continue


            print(f"Processing {subset}/{video_file}")
            rows = process_video(video_path, annotation_path, pose)
            all_rows.extend(rows)


    df = pd.DataFrame(all_rows)
    df.to_csv(output_csv, index = False)
    print(f"Saved {len(df)} rows to {output_csv}")

if __name__ == "__main__":
    build_dataset("data/le2i", "data/features.csv")        


