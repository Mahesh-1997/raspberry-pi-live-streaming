import cv2
import numpy
import psutil
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response, stream_with_context, request

video = cv2.VideoCapture("video-light.mp4")
app = Flask('__name__')


def video_stream():
    while True:
        ret, frame = video.read()
        if not ret:
            break;
        else:
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')


@app.route('/live-stream')
def live_stream():
    return render_template('live-stream.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port='5000', debug=False)
