import logging
from io import BytesIO

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import torch
import torchvision

from model import load_model_and_preprocess
from utils import filter_results


# Logger 설정
logger = logging.getLogger('uvicorn')
logger.setLevel(logging.DEBUG)

# FastAPI 앱 생성
logger.debug('Creating FastAPI app...')
app = FastAPI()
logger.debug('FastAPI app created.')

# 모델 불러오기
logger.debug('Initializing model...')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model, preprocess, meta = load_model_and_preprocess(device)
logger.debug(f'Model initialized successfully with device: {device}')

# 모델 정보 관리
models = [
  {
    'id': model.__class__.__module__,
    'name': type(model).__name__
  }
]


# 루트 엔드포인트
@app.get("/")
def root():
  logger.debug('Root endpoint called...')
  return JSONResponse(content={'Hello': 'World'})


# HTTP Health Probe
@app.get('/liveness')
def liveness():
  logger.debug('Health probe called...')
  return JSONResponse(content={'status': 'ok'})


# 모델 정보 엔드포인트
@app.get('/models')
def get_models():
  logger.debug('Returning model information...')
  return JSONResponse(content={'models': models})


# 객체 탐지 엔드포인트
@app.post('/image:detect')
def detect_objects(image: UploadFile, threshold: float = 0.5, klass: int = None):
  logger.debug('Detecting objects in the uploaded image...')
  logger.debug(f'Threshold: {threshold}, Class ID: {klass}')
  try:
    # 이미지 파일이 아닌 경우 예외 발생
    if not image.headers['content-type'].startswith('image/'):
      raise ValueError('Uploaded file is not an image')

    # 클래스 ID가 주어진 경우, 유효한 클래스 ID인지 확인
    if klass is not None and klass < 0:
      raise ValueError('Invalid class ID')

    # 업로드된 이미지 파일 열기 (PIL.Image 객체로 변환)
    img_obj = Image.open(BytesIO(image.file.read()))

    # 전처리
    img_input = preprocess(img_obj).to(device)
    img_input = img_input.unsqueeze(0) # 단일 이미지이므로 배치(batch) 차원 추가

    # 추론 수행
    outputs = model(img_input)[0] # 단일 이미지이므로 첫번째 결과만 사용

    # 결과 필터링
    results = filter_results(outputs, meta['categories'], threshold=threshold, klass=klass)

    # 결과 반환
    logger.debug(f'Objects detected: {len(results)}')
    return JSONResponse(content={'objects': results})

  except ValueError as e:
    logger.error(f'ValueError: {e}')
    return JSONResponse(content={'error': str(e)}, status_code=415)

  except Exception as e:
    logger.error(f'Error: {e}')
    return JSONResponse(content={'error': str(e)}, status_code=500)


if __name__ == '__main__':
  # 모델 불러오기
  logger.debug('Load & saving model...')
  load_model_and_preprocess()
  logger.debug('Model saved.')
