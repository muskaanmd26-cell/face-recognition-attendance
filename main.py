import cv2
import face_recognition
import numpy as np
import sqlite3
from datetime import datetime
import os

# ---------------- DATABASE ----------------

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    entry_time TEXT,
    status TEXT
)
""")

conn.commit()

# ---------------- LOAD KNOWN FACES ----------------

known_faces = []
known_names = []

# Folder containing registered student images
folder = "known_faces"

if not os.path.exists(folder):
    os.makedirs(folder)

for filename in os.listdir(folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        image_path = os.path.join(folder, filename)
        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_faces.append(encodings[0])

            # Filename becomes student's name
            name = os.path.splitext(filename)[0]
            known_names.append(name)

print("Known students:", known_names)

# ---------------- CAMERA ----------------

camera = cv2.VideoCapture(0)

marked_students = set()

print("Camera started...")
print("Press Q to quit.")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Unable to access camera.")
        break

    # Resize for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(
        rgb_frame,
        face_locations
    )

    for face_encoding, face_location in zip(
        face_encodings,
        face_locations
    ):

        if len(known_faces) == 0:
            name = "Unknown"
        else:
            matches = face_recognition.compare_faces(
                known_faces,
                face_encoding
            )

            face_distances = face_recognition.face_distance(
                known_faces,
                face_encoding
            )

            best_match = np.argmin(face_distances)

            if matches[best_match]:
                name = known_names[best_match]
            else:
                name = "Unknown"

        # ---------------- ATTENDANCE ----------------

        if name != "Unknown" and name not in marked_students:

            now = datetime.now()

            date = now.strftime("%Y-%m-%d")
            entry_time = now.strftime("%H:%M:%S")

            cursor.execute("""
            INSERT INTO attendance
            (name, date, entry_time, status)
            VALUES (?, ?, ?, ?)
            """, (name, date, entry_time, "Present"))

            conn.commit()

            marked_students.add(name)

            print(
                f"Attendance marked: {name} - {date} {entry_time}"
            )

        # ---------------- DRAW RESULT ----------------

        top, right, bottom, left = face_location

        # Scale coordinates back to original frame
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            name,
            (left, bottom + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Recognition Attendance", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
conn.close()