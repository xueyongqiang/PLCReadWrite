import cv2
import pyttsx3
import time

# 初始化语音
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # 语速

def say(text):
    engine.say(text)
    engine.runAndWait()

# 打开笔记本摄像头（0 就是自带摄像头）
cap = cv2.VideoCapture(0)

# 用人脸检测来判断有没有人
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

last_welcome = 0
cooldown = 5  # 5秒内不重复喊

print("已启动监控，有人就会播报")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # 画出人脸框
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 检测到人
    if len(faces) > 0:
        if time.time() - last_welcome > cooldown:
            say("欢迎光临，我已经看到你了")
            last_welcome = time.time()

    cv2.imshow("Camera Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()