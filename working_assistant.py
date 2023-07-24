import os
import time
import requests
import shutil
import subprocess
from flask import Flask, send_file, render_template_string
from threading import Thread

app = Flask(__name__)

url = "http://192.168.0.7/16"
save_dir = "./images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

inference_dir = "./runs/detect/predict"
if not os.path.exists(inference_dir):
    os.makedirs(inference_dir)

results = {"Normal": 0, "distraction": 0, "drowsiness": 0, "mobile": 0, "yawning": 0}

def fetch_image_and_inference():
    while True:
        # Fetch the image
        file_name = f"{save_dir}/image.jpg"
        response = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        
        print(f"Image saved to {file_name}")
        
        # Remove inference directory if it exists
        if os.path.exists(inference_dir):
            shutil.rmtree(inference_dir)

        # Run inference
        result = subprocess.run(
            ['yolo', 'task=detect', 'mode=predict', 'model=best.pt', 'conf=0.3', 'source=./images', 'save=True'],
            capture_output=True,
            text=True,
        )

        output = result.stdout
        for key in results.keys():
            if key in output:  # We no longer need to make it lower
                results[key] += 1
        
        time.sleep(10)


@app.route('/')
def serve_image():
    # Refresh the page every 10 seconds
    refresh_rate = 10  # in seconds
    return render_template_string("""
    <html>
        <head>
            <meta http-equiv="refresh" content="{{ refresh_rate }}">
        </head>
        <body>
            <img src="{{ url_for('get_inferred_image') }}" />
            <p>Normal: {{ results['Normal'] }}</p>
            <p>Drowsiness: {{ results['Drowsiness'] }}</p>
            <p>Mobile: {{ results['Mobile'] }}</p>
            <p>Distraction: {{ results['Distraction'] }}</p>
            <p>Yawning: {{ results['Yawning'] }}</p>
        </body>
    </html>
    """, refresh_rate=refresh_rate, results=results)

@app.route('/inferred_image.jpg')
def get_inferred_image():
    return send_file(f"{inference_dir}/image.jpg", mimetype='image/jpg')

if __name__ == '__main__':
    thread = Thread(target=fetch_image_and_inference)
    thread.start()
    app.run(host='0.0.0.0')
