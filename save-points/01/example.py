import torchvision
from torchvision.models.detection import retinanet_resnet50_fpn_v2, RetinaNet_ResNet50_FPN_V2_Weights

# 사전 학습 모델 및 정보 불러오기
def load_model_and_preprocess():
  weights = RetinaNet_ResNet50_FPN_V2_Weights.DEFAULT
  model = retinanet_resnet50_fpn_v2(weights=weights)
  model.eval()

  return model, weights.transforms(), weights.meta


# sample.jpg 이미지를 불러와서 모델에 입력으로 전달하고, 예측 결과를 출력
if __name__ == '__main__':
  model, preprocess, meta = load_model_and_preprocess()   # 모델 및 전처리 함수 등 불러오기

  img_tensor = torchvision.io.read_image('../sample.jpg') # 예제 이미지 불러오기

  input_batch = [preprocess(img_tensor)]  # 입력이 하나뿐이므로, list로 감싸서 묶음(batch)으로 만듦(비추천). 또는,
  # input_batch = preprocess(img_tensor).unsqueeze(0)  # unsqueeze()로 맨 앞에 차원을 추가해도 됨 (batch 차원)

  preds = model(input_batch)              # 입력을 모델에 전달하여 예측 결과 얻기
  prediction = preds[0]                   # 첫번째 입력에 해당하는 첫번째 결과 가져오기
  print('예측 결과: ')
  print(prediction)

  # 객체 ID를 순서대로 가져와 객체 이름을 매핑
  label_txts = [meta['categories'][class_id] for class_id in prediction['labels']]
  print(prediction['labels'], label_txts)   # Class ID 및 Label 확인

  # draw_bounding_boxes() 함수를 사용하여 탐지된 객체들의 위치를 표시합니다.
  tensor_with_boxes = torchvision.utils.draw_bounding_boxes(img_tensor,
                            boxes=prediction['boxes'],
                            labels=label_txts,
                            colors='red',
                            width=2)

  # draw_bounding_boxes()는 Tensor를 반환하므로, 시각화를 위해 PIL.Image로 변환합니다.
  img_with_boxes = torchvision.transforms.v2.functional.to_pil_image(tensor_with_boxes)
  img_with_boxes.save('sample_output.jpg') # 결과 이미지 저장
