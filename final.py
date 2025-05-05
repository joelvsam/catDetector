from flask import Flask, Response, render_template_string, request, redirect
from gpiozero import MotionSensor
from ultralytics import YOLO
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import cv2
import time
import threading
import atexit

app = Flask(__name__)

# YOLO model
model = YOLO("best.pt")

# Global state
pir_enabled = True
buzzer_enabled = True
motion_detected = False

# Initialize PIR sensor
pir = MotionSensor(12)

# Initialize camera once
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(0.5)

# Setup passive buzzer on GPIO18
buzzer_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
buzzer_pwm = GPIO.PWM(buzzer_pin, 1000)
buzzer_pwm.start(0)

def buzz(duration=0.5, frequency=1000):
    if buzzer_enabled:
        buzzer_pwm.ChangeFrequency(frequency)
        buzzer_pwm.ChangeDutyCycle(50)
        time.sleep(duration)
        buzzer_pwm.ChangeDutyCycle(0)

# GPIO cleanup
def cleanup():
    print("Cleaning up GPIO...")
    buzzer_pwm.stop()
    GPIO.cleanup()

atexit.register(cleanup)

# PIR motion logic
def motion_handler():
    global motion_detected
    while True:
        if pir_enabled:
            pir.wait_for_motion()
            motion_detected = True
            time.sleep(10)
            motion_detected = False
        else:
            time.sleep(0.5)

motion_thread = threading.Thread(target=motion_handler)
motion_thread.daemon = True
motion_thread.start()

# Frame generator
def generate_frames():
    while True:
        if pir_enabled and not motion_detected:
            time.sleep(0.1)
            continue

        frame = picam2.capture_array()
        results = model(frame)
        result = results[0]
        names = model.names
        boxes = result.boxes

        cat_count = 0

        if boxes:
            for box in boxes:
                cls_id = int(box.cls[0])
                class_name = names[cls_id]
                if class_name.lower() == "cat":
                    cat_count += 1
                    buzz(duration=0.5, frequency=1000)

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, class_name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Overlay cat count
        cv2.putText(frame, f"Number of cats: {cat_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Motion status route
@app.route('/motion_status')
def motion_status():
    return {"motion": motion_detected}

# Web UI
@app.route('/', methods=["GET", "POST"])
def index():
    global pir_enabled, buzzer_enabled

    if request.method == "POST":
        if "toggle_pir" in request.form:
            pir_enabled = not pir_enabled
        elif "toggle_buzzer" in request.form:
            buzzer_enabled = not buzzer_enabled
        return redirect("/")

    return render_template_string("""
        <html>
            <head>
                <title>Live Cat Detection</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; background-color: #f0f0f0; }
                    h1 { color: #333; }
                    button { padding: 10px 20px; font-size: 16px; margin: 10px; }
                    img { border: 2px solid #444; margin-top: 10px; }
                    #motion-status { font-size: 20px; color: #d00; margin-top: 10px; }
                </style>
            </head>
            <body>
                <h1>Live Cat Detection Feed</h1>
                <form method="post">
                    <button name="toggle_pir" type="submit">
                        {{ 'Disable PIR Sensor' if pir_enabled else 'Enable PIR Sensor' }}
                    </button>
                    <button name="toggle_buzzer" type="submit">
                        {{ 'Disable Buzzer' if buzzer_enabled else 'Enable Buzzer' }}
                    </button>
                </form>
                <div id="motion-status">Motion: Checking...</div>
                <img src="{{ url_for('video_feed') }}" width="640" height="480">

                <script>
                    function checkMotion() {
                        fetch('/motion_status')
                            .then(response => response.json())
                            .then(data => {
                                const status = data.motion ? "Motion Detected!" : "No Motion";
                                const color = data.motion ? "#d00" : "#333";
                                document.getElementById("motion-status").textContent = "Motion: " + status;
                                document.getElementById("motion-status").style.color = color;
                            })
                            .catch(error => {
                                document.getElementById("motion-status").textContent = "Motion: Error";
                            });
                    }
                    setInterval(checkMotion, 1000);
                </script>
            </body>
        </html>
    """, pir_enabled=pir_enabled, buzzer_enabled=buzzer_enabled)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
