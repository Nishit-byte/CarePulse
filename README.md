# 💛 CarePulse

**AI-powered fall detection and elder care monitoring, right from a webcam.**

CarePulse watches a live camera feed, uses pose estimation and a trained classifier to recognize when someone has fallen, waits to confirm it isn't a false alarm, and then alerts a caregiver over WhatsApp — all while logging everything to a Streamlit dashboard so families and caregivers can track history, manage devices, and monitor multiple people from one place.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Clone & Install](#2-clone--install)
  - [3. Configure Environment Variables](#3-configure-environment-variables)
  - [4. Initialize the Database](#4-initialize-the-database)
  - [5. Train the Fall Detection Model](#5-train-the-fall-detection-model)
  - [6. Run the Dashboard](#6-run-the-dashboard)
  - [7. Run Live Fall Detection](#7-run-live-fall-detection)
- [Configuring Alerts (Twilio WhatsApp)](#configuring-alerts-twilio-whatsapp)
- [Detection Sensitivity](#detection-sensitivity)
- [Database Schema](#database-schema)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)

---

## How It Works

1. **Pose extraction** — [MediaPipe Pose](https://developers.google.com/mediapipe) tracks 33 body landmarks per frame from a webcam feed.
2. **Feature engineering** — `pose_utils.py` converts raw landmarks into interpretable features: torso angle, bounding-box aspect ratio, normalized hip height, shoulder–hip distance, and frame-to-frame velocity.
3. **Classification** — A `RandomForestClassifier` (scikit-learn), trained on the [Le2i Fall Detection Dataset](https://search.kaggle.com/), predicts whether the current pose looks like a fall.
4. **Confirmation window** — A fall "candidate" only becomes a confirmed alert if the person then stays motionless for a configurable number of seconds (default 10s), which cuts down on false positives from sitting or bending down quickly.
5. **Alerting** — Once confirmed, CarePulse logs the incident to SQLite and sends a WhatsApp message via Twilio to the registered emergency contact.
6. **Dashboard** — A Streamlit app lets caregivers sign up, add monitored persons and camera devices, review live status, resolve alerts, and browse historical trends.

---

## Features

- 🔐 **Accounts** — simple username/password signup & login (SHA-256 hashed) backed by SQLite
- 🧍 **Multi-person monitoring** — track several people, each assigned to a room and a device
- 🎥 **Device management** — scan for connected webcams and register them as monitoring devices
- 🤖 **ML-based fall detection** — Random Forest classifier over pose-derived features, with a rule-based motionless-confirmation stage to reduce false alarms
- 📲 **WhatsApp emergency alerts** — automatic message via Twilio when a fall is confirmed
- 📊 **Dashboard** — live stats: monitored persons, active alerts, devices online, falls this month
- 🕑 **History & Reports** — timeline charts of falls over time, resolution rates, and average detection confidence
- ⚙️ **Tunable sensitivity** — adjust the motionless-confirmation window per account from Settings
- 🌱 **Demo data seeding** — populate the app with sample people and past alerts for demos/testing

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI / Dashboard | [Streamlit](https://streamlit.io/) |
| Computer Vision | [OpenCV](https://opencv.org/), [MediaPipe Pose](https://developers.google.com/mediapipe) |
| ML | scikit-learn (Random Forest), joblib, pandas, numpy |
| (Optional) Sequence modeling | TensorFlow (LSTM/GRU upgrade path) |
| Database | SQLite (`sqlite3`, no external DB server needed) |
| Alerts | [Twilio WhatsApp API](https://www.twilio.com/whatsapp) |
| Charts | Matplotlib |
| Config | python-dotenv |

---

## Project Structure

```
CarePulse-main/
├── app.py                  # Streamlit entry point & page navigation
├── database.py              # SQLite schema + all data-access functions
├── fall_detection_ml.py     # Live webcam loop: pose → features → prediction → alert
├── pose_utils.py            # Landmark → feature extraction (angles, ratios, velocity)
├── dataset_builder.py        # Builds a labeled feature CSV from the Le2i video dataset
├── train_model.py           # Trains & saves the Random Forest fall classifier
├── seed_data.py              # Seeds the DB with demo people, devices, and alerts
├── style.py                  # Shared CSS/theme + sidebar components for Streamlit pages
├── requirements.txt
├── screens/
│   ├── landing.py            # Public landing page
│   ├── login.py               # Login screen
│   ├── signup.py              # Signup screen
│   ├── dashboard.py           # Overview: stats, recent alerts
│   ├── alerts.py               # Full alert list + detail/resolve view
│   ├── history.py              # Fall activity over time (chart)
│   ├── users.py                # Manage monitored persons
│   ├── devices.py              # Manage/scan camera devices
│   ├── reports.py              # Aggregate insights (totals, resolution rate, confidence)
│   └── settings.py             # Account, emergency contact, detection sensitivity
└── data/                     # (generated) SQLite DB, datasets, feature CSVs
```

> `data/` and `models/` are created at runtime and are git-ignored — see [Getting Started](#getting-started) below.

---

## Getting Started

### 1. Prerequisites

- Python 3.9–3.11 (MediaPipe/TensorFlow compatibility)
- A webcam (for live detection)
- A [Twilio](https://www.twilio.com/) account with WhatsApp sandbox/sender enabled (for alerts)
- *(Optional)* A [Kaggle](https://www.kaggle.com/) account + API key if you want to rebuild the training dataset from scratch

### 2. Clone & Install

```bash
git clone https://github.com/<your-username>/CarePulse.git
cd CarePulse

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
TWILIO_SID=your_twilio_account_sid
TWILIO_AUTH=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+91XXXXXXXXXX
```

If these are left unset, the app still runs — the detection loop will simply skip sending WhatsApp messages and print a warning instead.

### 4. Initialize the Database

The SQLite database (`data/care.db`) is created automatically the first time the app runs `init_db()`. To also populate it with demo people, devices, and past alerts for a quick test drive:

```bash
python seed_data.py
```

### 5. Train the Fall Detection Model

CarePulse ships **without** a pre-trained model — you need to build the dataset and train it once before live detection will work.

```bash
# 1. Download the Le2i Fall Detection Dataset into data/le2i/
#    (requires a Kaggle API key configured at ~/.kaggle/kaggle.json)

# 2. Extract pose features from every video into a labeled CSV
python dataset_builder.py
# → writes data/features.csv

# 3. Train the Random Forest classifier
python train_model.py
# → writes models/fall_classifier.pkl
```

### 6. Run the Dashboard

```bash
streamlit run app.py
```

Sign up for an account, then head to **Users** to add the person(s) you want to monitor and **Devices** to register a webcam.

### 7. Run Live Fall Detection

In a separate terminal (with the same virtual environment active):

```bash
python fall_detection_ml.py <your_username>
```

This opens your webcam, runs pose estimation frame-by-frame, and will:
- Flag a **fall candidate** as soon as the classifier predicts a fall
- Start a motionless-confirmation timer
- Log a confirmed alert to the database and send a WhatsApp message once the timer elapses
- Automatically resolve the alert in the dashboard once the person moves again

Press **`q`** in the video window to stop monitoring.

---

## Configuring Alerts (Twilio WhatsApp)

1. Create a free [Twilio](https://www.twilio.com/) account and join the WhatsApp Sandbox (or provision a WhatsApp sender for production).
2. Copy your **Account SID** and **Auth Token** into `.env`.
3. Set `TWILIO_WHATSAPP_FROM` to your Twilio WhatsApp number and `TWILIO_WHATSAPP_TO` to the caregiver's number, both prefixed with `whatsapp:`.
4. You can view/update the destination number from the **Settings** page in the app — note that this is a display-only convenience; the number actually used is read from `.env` at process start, so update `.env` and restart the app for changes to take effect.

---

## Detection Sensitivity

Every account has a **motionless confirmation window** (default: 10 seconds, adjustable 3–20s from **Settings → Detection Sensitivity**). After a fall is predicted, the person must remain still for this long before an alert fires — a shorter window reacts faster but risks more false alarms; a longer window is more conservative.

---

## Database Schema

CarePulse uses a lightweight SQLite database with four tables:

| Table | Purpose |
|---|---|
| `users` | Account credentials + per-user detection sensitivity (`motionless_seconds`) |
| `devices` | Camera devices, each tied to a room and a user |
| `persons` | Monitored individuals, each tied to a device/room; one person per user can be flagged `is_live` (the one tracked by the local webcam) |
| `alerts` | Logged fall events with timestamp, confidence score, priority, and resolution status |

---

## Roadmap

- [ ] Upgrade from single-frame Random Forest to a sequence model (LSTM/GRU) using pose trajectories over time
- [ ] Multi-camera support for simultaneous live monitoring of several people
- [ ] SMS/phone-call fallback alerts in addition to WhatsApp
- [ ] Cloud deployment guide (currently designed for local/on-premise use)

---

## Disclaimer

CarePulse is an educational/portfolio project and **is not a certified medical device**. It should not be relied upon as a sole safety measure for vulnerable individuals. Always pair automated monitoring with human caregiving plans and emergency services.
