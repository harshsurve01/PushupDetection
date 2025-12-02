# PushupDetection

A Python application that uses **OpenCV** and **CVZone Pose Detection** to count push-ups in real-time with proper form using a webcam. The app also includes a **Kivy GUI** to display push-up counts and a reward screen for lifetime push-ups.

---

## Table of Contents

* Features
* Installation
* Usage
* How It Works
* Folder Structure
* Dependencies
* License
* Contact

---

## Features

* Count push-ups in real-time using pose estimation.
* Display a live camera feed with push-up detection overlay.
* Countdown timer before starting the session.
* Detects correct push-up form: horizontal body and elbow angles.
* Rewards screen showing total lifetime push-ups.

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/harshsurve01/PushupDetection.git
cd PushupDetection
```

2. **Install dependencies:** Ensure you have Python 3.8+ installed. Then install the required packages:

```bash
pip install opencv-python
pip install cvzone
pip install numpy
pip install kivy
```

---

## Usage

1. Run the application:

```bash
python main.py
```

2. Click **Start Pushup Session** and get into position.

3. The app will count your push-ups automatically based on proper form.


---

## How It Works

* Uses **CVZone PoseModule** to detect body landmarks (shoulders, elbows, hips).
* Calculates **elbow angles** to determine the push-up movement.
* Checks **horizontal alignment** of the body using shoulder and hip positions.
* Counts push-ups only when proper form is maintained and ensures a minimum time between repetitions to avoid double counting.

---

## Folder Structure

```
PushupDetection/
│
├─ pushups.py           # Main application code
├─ README.md         # This readme file
```

---

## Dependencies

* Python 3.8+
* [OpenCV](https://pypi.org/project/opencv-python/)
* [CVZone](https://pypi.org/project/cvzone/)
* [NumPy](https://pypi.org/project/numpy/)
* [Kivy](https://kivy.org/#home)

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Contact

**Harsh Surve**

* GitHub: [harshsurve01](https://github.com/harshsurve01)
* Email: [surveharsh04@gmail.com](mailto:surveharsh04@gmail.com)
