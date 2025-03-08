import cv2
from cvzone.PoseModule import PoseDetector
import numpy as np
import time
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup

class PushupScreen(Screen):
    def __init__(self, **kwargs):
        super(PushupScreen, self).__init__(**kwargs)
        self.pushup_count = 0
        self.detector = PoseDetector()
        self.cap = None
        self.pushup_position = "up"  # Start in the "up" position
        self.threshold_angle = 45  # Threshold angle to determine the push-up position
        self.min_time_between_pushups = 1.5  # Minimum time in seconds between successive push-ups
        self.last_pushup_time = 0  # Time of the last counted push-up

        layout = BoxLayout(orientation='vertical')
        self.count_label = Label(text="Push-Ups: 0")
        layout.add_widget(self.count_label)
        self.start_button = Button(text="Start Pushup Session")
        self.start_button.bind(on_release=self.start_pushup_session)
        layout.add_widget(self.start_button)
        self.add_widget(layout)

    def start_pushup_session(self, instance):
        popup = Popup(title='Get Ready!', content=Label(text='You have 5 seconds to get into position.'), size_hint=(0.7, 0.7))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2.5)
        self.start_camera()
        Clock.schedule_once(self.start_countdown, 2.5)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_camera_feed, 1/30)  # Update camera feed every 1/30 sec

    def start_countdown(self, dt):
        self.countdown_value = 5  # Countdown starts from 5 seconds
        Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        if self.countdown_value > 0:
            self.count_label.text = f"Starting in {self.countdown_value}..."
            self.countdown_value -= 1
        else:
            self.count_label.text = "Push-up session started!"
            Clock.unschedule(self.update_countdown)
            Clock.schedule_interval(self.detect_pushups, 1/30)

    def update_camera_feed(self, dt):
        if self.cap:
            success, img = self.cap.read()
            if success:
                # Update the camera feed in a window
                cv2.imshow("Pushup Detection", img)
                # Draw the countdown on the camera feed
                if hasattr(self, 'countdown_value') and self.countdown_value > 0:
                    cv2.putText(img, f"Starting in {self.countdown_value}...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow("Pushup Detection", img)

    def calculate_angle(self, a, b, c):
        angle = np.arctan2(c[2] - b[2], c[1] - b[1]) - np.arctan2(a[2] - b[2], a[1] - b[1])
        return np.abs(angle * 180.0 / np.pi)

    def is_horizontal(self, shoulder_left, shoulder_right, hip_left, hip_right):
        shoulder_mid = (shoulder_left[2] + shoulder_right[2]) / 2
        hip_mid = (hip_left[2] + hip_right[2]) / 2
        return abs(shoulder_mid - hip_mid) < 50

    def detect_pushups(self, dt):
        if self.cap:
            success, img = self.cap.read()
            if success:
                img = self.detector.findPose(img)
                lmList, bboxInfo = self.detector.findPosition(img, bboxWithHands=False)

                if lmList:
                    shoulder_left = lmList[11]  # Left shoulder
                    shoulder_right = lmList[12]  # Right shoulder
                    elbow_left = lmList[13]  # Left elbow
                    elbow_right = lmList[14]  # Right elbow
                    hip_left = lmList[23]  # Left hip
                    hip_right = lmList[24]  # Right hip

                    left_arm_angle = self.calculate_angle(shoulder_left, elbow_left, hip_left)
                    right_arm_angle = self.calculate_angle(shoulder_right, elbow_right, hip_right)

                    current_time = time.time()
                    if left_arm_angle < self.threshold_angle and right_arm_angle < self.threshold_angle and self.is_horizontal(shoulder_left, shoulder_right, hip_left, hip_right):
                        if self.pushup_position == "up" and (current_time - self.last_pushup_time) > self.min_time_between_pushups:
                            self.pushup_count += 1
                            self.pushup_position = "down"
                            self.last_pushup_time = current_time
                    elif left_arm_angle > self.threshold_angle and right_arm_angle > self.threshold_angle:
                        self.pushup_position = "up"

                    self.count_label.text = f"Push-Ups: {self.pushup_count}"

                cv2.imshow("Pushup Detection", img)

    def on_leave(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

class RewardScreen(Screen):
    def __init__(self, **kwargs):
        super(RewardScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.reward_label = Label(text="Lifetime Pushups: 0")
        layout.add_widget(self.reward_label)
        self.add_widget(layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PushupScreen(name='pushup'))
        sm.add_widget(RewardScreen(name='reward'))
        return sm

if __name__ == '__main__':
    MyApp().run()
