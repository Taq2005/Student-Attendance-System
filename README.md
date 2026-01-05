# 🎓 Face Recognition Attendance System

A **desktop-based Face Recognition Attendance System** built using **Python, OpenCV, Tkinter, and Supabase**. The system allows automatic student attendance using face recognition, along with an **Admin Panel** to manage student records.
---

## 🚀 Features

### 👨‍🎓 Student Attendance

* Real-time face recognition using webcam
* Automatic attendance marking
* Prevents duplicate attendance using time checks
* Displays student details and photo

### 🔐 Admin Panel (Password Protected)

* Add new students
* View database online (Supabase)
* Edit existing student records
* Upload and manage student photos

### 🖼 Image Handling

* Accepts **square images only (1:1 ratio)**
* Automatically resizes images to **128×128**
* Stores images securely in Supabase Storage

---

## 🛠️ Tech Stack

* **Python 3.9+**
* **OpenCV** – image processing
* **face-recognition** – face encoding & matching
* **Tkinter** – GUI
* **Supabase** – database & storage
* **NumPy**
* **cvzone**

---

## 📁 Project Structure

```
Face-Recognition-Attendance/
│
├── attendance.py          # Face recognition & attendance logic
├── admin.py               # Admin panel UI
├── main.py                # Main application launcher
├── Supabase_client.py     # Supabase connection
├── serviceAcc.py          # Supabase URLs & keys
├── Encode.pickle          # Face encodings
├── requirements.txt
│
├── Resources/
│   ├── background.jpg
│   └── Modes/
│       ├── mode1.png
│       ├── mode2.png
│       └── ...
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Supabase

* Create a Supabase project
* Create a **Students** table
* Create an **Images** storage bucket
* Add your credentials in:

  * `Supabase_client.py`
  * `serviceAcc.py`

---

## ▶️ Run the Application

```bash
python main.py
```

---

## 🧑‍💻 Admin Credentials

> Default password (can be changed in code):

```
admin123
```

Max attempts: **3**

---

## 🧠 Future Improvements

* Blink / liveness detection (anti-proxy)
* Multiple face detection
* Attendance reports export
* Role-based access control
* Web-based dashboard

---

## 📊 KPIs (Key Performance Indicators)

* Face recognition accuracy
* Attendance marking time
* False positive rate
* Admin task completion time

---

## 🙏 Acknowledgements

Thanks to open-source libraries and Supabase for backend services.

> **JazakAllahu Khairan❤️**

---
## 📬 Contact

If you have suggestions or improvements, feel free to reach out!
