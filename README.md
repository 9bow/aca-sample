# Deploy PyTorch App on Azure Container Apps

## 소개

이 저장소는 Azure Container Apps에 PyTorch 애플리케이션을 배포하는 방법을 보여주는 예제로, torchvision이 제공하는 사전 학습된 PyTorch 모델을 사용하여 이미지에서 객체를 감지하는 간단한 REST API를 포함하고 있습니다.

**Disclaimer**: 이 저장소의 모든 코드는 교육 목적으로 작성하였으며, 서비스를 고려하지 않았습니다. 모든 코드는 보안, 성능, 확장성 등을 고려하지 않았으며, 실제 서비스에 사용하시면 안됩니다.


## 준비사항

- Python 3.10 이상 및 가상환경
  - Anaconda 또는 miniconda 설치를 추천합니다: [Anaconda 또는 miniconda 설치](https://www.anaconda.com/download)
  - (선택사항) (conda 미사용 시) pyenv 등을 사용하여 가상 환경을 구성합니다.
  -  `python -V` 명령어를 실행했을 때 Python 3.10 이상이 출력되어야 합니다.
- Azure 계정
  - Azure Portal에 로그인할 수 있는 계정이 필요합니다: [Azure Portal](https://portal.azure.com)
  - 유효한 구독이 있어야 합니다.
- GitHub 계정 및 Git Client
  - GitHub에 로그인할 수 있는 계정이 필요합니다: [GitHub](https://github.com)
  - GitHub에 로그인, 저장소 만들기, Commit 및 Push가 가능해야 합니다.
  - `git` 명령어를 실행했을 때 동작해야 합니다: [Git 설치](https://git-scm.com/downloads)
- Visual Studio Code (또는 코드 에디터)
  - Visual Studio Code를 사용하는 것을 추천합니다: [Visual Studio Code 설치](https://code.visualstudio.com/download)
  - (Visual Studio Code 사용 시) Python Extension Pack 설치를 추천합니다: [Python Extension Pack](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack)
- Docker 또는 Podman 등
  - Docker 또는 Podman을 사용하여 컨테이너 이미지를 빌드하고 실행할 수 있어야 합니다: [Docker 설치](https://docs.docker.com/get-docker/)


## 주요 내용

- PyTorch, 객체 탐지 작업 및 사전 학습 모델 소개
- Sample App 소개: FastAPI를 사용한 API Server
- Container 소개
- Sample App을 Container Image로 만들기 & 실행하기
- Azure Container Apps 소개
- Azure Container Apps에 Sample App 배포하기


## 샘플 이미지 출처

- client/data/sample.jpg: https://unsplash.com/photos/a-group-of-people-walking-down-a-flight-of-stairs-jEEP-bzH3jI
- save-points/sample.jpg: https://unsplash.com/photos/a-man-standing-on-a-set-of-stairs-using-a-cell-phone-VsDV9j30Sww
- save-points/sample2.jpg: https://unsplash.com/photos/a-couple-of-people-walking-down-a-sidewalk-kIuAm7aIDQQ
- save-points/sample3.jpg: https://unsplash.com/photos/a-group-of-people-walking-along-a-river-next-to-tall-buildings-c91mpA0KwZ4
