# Python:3.10 이미지를 가져와서 이것을 기반으로 구성
FROM python:3.10
WORKDIR /app

# 의존성을 정의한 requirements.txt 파일 복사
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 나머지 파일 복사
COPY . .
RUN python3 app.py   # /root/.cache/torch/hub/checkpoints/retinanet_resnet50_fpn_v2_coco-5905b1c5.pth

# 그 외 실행 옵션
EXPOSE 80
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
