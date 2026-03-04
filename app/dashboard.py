import streamlit as st
import cv2
from deepface import DeepFace

st.title("InterviewIQ - AI Emotion & Confidence Analyzer")

st.write("Real-time emotion analysis for mock interview evaluation.")

start = st.button("Start Camera")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

if start:

    cap = cv2.VideoCapture(0)
    FRAME_WINDOW = st.image([])

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            face_img = frame[y:y+h, x:x+w]

            try:

                result = DeepFace.analyze(
                    face_img,
                    actions=['emotion'],
                    enforce_detection=False
                )

                emotions = result[0]['emotion']

                happy_score = emotions["happy"]
                surprise_score = emotions["surprise"]

                dominant_emotion = max(emotions, key=emotions.get)
                confidence = emotions[dominant_emotion]

                # Surprise correction rule
                if surprise_score > 25 and abs(happy_score - surprise_score) < 20:
                    dominant_emotion = "surprise"
                    confidence = surprise_score

                # Threshold filter
                if confidence < 40:
                    dominant_emotion = "neutral"

                # Interview confidence logic
                if dominant_emotion in ["happy", "surprise"]:
                    interview_level = "High Confidence"
                elif dominant_emotion == "neutral":
                    interview_level = "Moderate Confidence"
                else:
                    interview_level = "Low Confidence"

                # Draw face box
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                cv2.putText(frame,
                            f"Emotion: {dominant_emotion}",
                            (x,y-40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0,255,0),
                            2)

                cv2.putText(frame,
                            f"Confidence: {confidence:.1f}%",
                            (x,y-15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0,255,0),
                            2)

                cv2.putText(frame,
                            f"Interview Level: {interview_level}",
                            (x,y+h+25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255,255,0),
                            2)

            except:
                pass

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(rgb_frame)

    cap.release()