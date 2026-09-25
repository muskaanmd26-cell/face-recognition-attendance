Face Recognition Attendance System 🎓🔐

An AI-based smart classroom attendance system that uses face recognition to automatically identify students and record their attendance with date and time.

📌 Project Overview

This project is designed to make classroom attendance faster, easier, and more automated. The system detects students using a camera, recognizes registered faces, and stores their attendance information in a database.

🚀 Features

- Face detection and recognition
- Automatic attendance marking
- Date and time recording
- Student database management
- Attendance status tracking
- Camera-based real-time recognition
- SQLite database for storing records

🛠️ Technologies Used

- Python
- OpenCV
- face_recognition
- NumPy
- SQLite
- YOLO

⚙️ How It Works

1. The camera captures the student's face.
2. The system detects the face.
3. The detected face is compared with registered faces.
4. If the student is recognized, attendance is automatically recorded.
5. The attendance record is stored in the SQLite database.
6. The system records information such as name, subject, date, entry time, exit time, and status.

📂 Project Structure

face-recognition-attendance/
│
├── main.py
├── database.py
├── requirements.txt
├── README.md
│
├── known_faces/
│   └── student_images/
│
└── screenshots/

🗄️ Attendance Database

The system can store:

Field| Description
Name| Student name
Subject| Class/subject
Date| Attendance date
Entry Time| Time of entry
Exit Time| Time of exit
Status| Present/Absent

🔮 Future Scope

- Liveness detection
- Anti-spoofing protection
- Mask detection
- Web-based attendance dashboard
- Cloud database integration
- Automated attendance reports

👩‍💻 Author

Muskaan

B.Tech Cybersecurity Student

Interested in Cybersecurity, Ethical Hacking, AI and Computer Vision