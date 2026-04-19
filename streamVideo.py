from flask import Flask, render_template_string, Response
import cv2

app = Flask(__name__)

def get_camera_index():
    """Automatically detect the USB webcam index."""
    # Try indices 0 to 4
    for index in range(5):
        cap = cv2.VideoCapture(index)
        if cap is not None and cap.isOpened():
            cap.release()
            return index
    return -1

# Initialize the camera
camera_index = get_camera_index()
if camera_index == -1:
    raise Exception("No webcam found. Please connect a USB webcam.")
camera = cv2.VideoCapture(camera_index)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <title>USB Webcam Live Stream</title>
    </head>
    <body>
        <h1>USB Webcam Live Stream</h1>
        <img src="{{ url_for('video_feed') }}" width="640" height="480">
    </body>
    </html>
    ''')

def gen_frames():
    """Video streaming generator function."""
    while True:
        success, frame = camera.read()  # Capture frame-by-frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)  # Encode frame in JPEG format
            frame = buffer.tobytes()
            # Concatenate frame data in HTTP multipart format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=False)
    finally:
        # Release the camera when the app is stopped
        camera.release()
