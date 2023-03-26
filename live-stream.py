import cv2
import numpy
import psutil
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response, stream_with_context, request

video = cv2.VideoCapture("trim.mp4")
app = Flask('__name__')

def video_stream():
    i = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        else:
            cpu_usage = psutil.cpu_percent()
            mem_usage = psutil.virtual_memory().percent
            # Creating the scatter plot
            plt.scatter(i, cpu_usage, color = "red")
            plt.scatter(i, mem_usage, color = "blue")
            plt.legend(["CPU", "Memory"], loc ="lower right")
            i+=1
            # plt.pause(0.1)

            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')
    plt.savefig('my_plot.png')
    plt.close()


@app.route('/live-stream')
def live_stream():
    return render_template('live-stream.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(host='0.0.0.0', port='5000', debug=False)
