import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose

def get_landmark_point(landmarks, idx, w, h):
    lm = landmarks[idx]
    return np.array([lm.x * w, lm.y * h])

def compute_torso_angle(shoulder_center, hip_center):
    dx = hip_center[0] - shoulder_center[0]
    dy = hip_center[1] - shoulder_center[1]
    return np.degrees(np.arctan2(abs(dx), abs(dy) + 1e-6))

def compute_bbox_aspect_ratio(landmarks, w, h):
    xs = [lm.x * w for lm in landmarks]
    ys = [lm.y * h for lm in landmarks]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    return width / (height + 1e-6)

def extract_features(landmarks, w, h, prev_hip_center):
    left_hip = get_landmark_point(landmarks, mp_pose.PoseLandmark.LEFT_HIP.value, w, h)
    right_hip = get_landmark_point(landmarks, mp_pose.PoseLandmark.RIGHT_HIP.value, w, h)
    left_shoulder = get_landmark_point(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER.value, w, h)
    right_shoulder = get_landmark_point(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER.value, w, h)

    hip_center = (left_hip + right_hip) / 2
    shoulder_center = (left_shoulder + right_shoulder) / 2

    aspect_ratio = compute_bbox_aspect_ratio(landmarks, w, h)
    torso_angle = compute_torso_angle(shoulder_center, hip_center)
    hip_y_norm = hip_center[1] / h
    shoulder_hip_dist_norm = np.linalg.norm(shoulder_center - hip_center) / h

    velocity = 0.0
    if prev_hip_center is not None:
        velocity = np.linalg.norm(hip_center - prev_hip_center) / h

    features = {
        "aspect_ratio": aspect_ratio,
        "torso_angle": torso_angle,
        "hip_y_norm": hip_y_norm,
        "shoulder_hip_dist_norm": shoulder_hip_dist_norm,
        "velocity": velocity,
    }
    return features, hip_center