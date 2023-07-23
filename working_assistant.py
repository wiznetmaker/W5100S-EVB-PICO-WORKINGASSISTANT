import time
import requests
import os
from collections import deque

url = "http://192.168.0.7/16"
save_dir = "./images"

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

i = 0
file_queue = deque(maxlen=5)
while True:
    # 이미지 다운로드
    file_name = f"{save_dir}/image_{i}.jpg"
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    
    # 파일 이름을 큐에 추가
    file_queue.append(file_name)
    
    # 5개 이상의 이미지가 있다면 가장 오래된 이미지 삭제
    while len(file_queue) > 5:
        os.remove(file_queue.popleft())
    
    time.sleep(2)
    i += 1
