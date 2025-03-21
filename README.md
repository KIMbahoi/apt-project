# 🏢 Smart Apartment Management System - 보안 & 게이트 제어 모듈

이 레포지토리는 **스마트 아파트 관리 시스템** 프로젝트의 일부인 **보안 시스템 및 게이트 제어 모듈**을 다룹니다.  
본 모듈은 머신러닝 기반의 객체 감지 기능과 ROS 및 Arduino 연동을 통해 **출입 제어**, **위험 요소 감지**, **실시간 알림**을 수행합니다.

---

## 🌐 프로젝트 개요 (전체 시스템 중 일부)

> **스마트 아파트 관리 시스템**은 자동 순찰, 보안, 물류 운송, 실시간 웹페이지로 구성된 통합 관리 플랫폼입니다.  
> 본 레포지토리는 이 중에서 **보안 시스템 및 게이트 제어** 기능을 담당합니다.

### ✨ 주요 기능 (본 모듈 기준)

1. **객체 감지 기반 차단기 제어**
   - YOLO 기반 모델로 특정 객체(사람, 칼 등) 인식 시 차단기를 자동으로 제어 (RAISE / LOWER)

2. **위험 요소 감지 및 경보**
   - ‘칼’과 같은 위험 요소를 탐지하면 자동으로 부저 작동 및 관리자 알림 전송

3. **ROS 연동 감지 결과 송신**
   - 감지된 객체 정보를 ROS Topic으로 전달해 통합 시스템과 연동

4. **웹 기반 수동 제어 (Web Serial API)**
   - 웹페이지 상에서 버튼 클릭으로 시리얼을 통해 게이트 수동 조작

---

## 🧱 주요 구성 요소

| 파일명              | 설명 |
|-------------------|------|
| `machine_police.py` | 칼 탐지 및 ROS, 부저 연동 |
| `machine_gate.py`   | 객체 인식 후 HTTP로 차단기 제어 |
| `crossing_gate.py`  | YOLO 감지 → 시리얼 명령으로 게이트 제어 |
| `gate_control.js`   | 웹페이지 상의 시리얼 통신 게이트 제어 |

---

## 🤖 사용된 모델

- `knife.pt`: 칼 감지 YOLO 모델
- `people.pt`: 사람 형상 감지
- `nano5.pt`: 특정 캐릭터 기반 클래스 분류

---

## 🔍 모듈별 상세 기능 설명
### 🛡️ 1. machine_police.py – 위험 감지 & 경보 시스템
Jetbot에서 실시간 영상 스트리밍 수신
YOLOv8으로 ‘knife(칼)’ 객체 탐지
신뢰도 0.9 이상이면:
부저 자동 작동 (5초간)
감지된 이미지 저장
ROS 토픽(/yolo_detection_results)으로 감지 정보 전송
### 🚪 2. machine_gate.py – 무선 게이트 제어 시스템
YOLO 모델로 사람 형태 객체 탐지
신뢰도 0.9 이상 시:
아두이노 웹서버에 HTTP 요청 전송 (RAISE 명령)
차단기 상승
### 🧱 3. crossing_gate.py – 시리얼 기반 게이트 제어 시스템
YOLO 모델로 지정 객체 탐지 (예: bunchiko, dragonite 등)
감지되면 아두이노 시리얼 포트에 명령 전송 (RAISE\n)
일정 시간 간격으로만 중복 제어 방지
### 🌐 4. gate_control.js – 브라우저 기반 수동 게이트 제어
사용자가 웹페이지에서 "Raise" 또는 "Lower" 버튼 클릭 시
Web Serial API를 통해 시리얼 포트로 명령 전송
상태 표시 및 버튼 활성화 처리 포함

---

## 🛠️ 기술 스택

- **언어/프레임워크**: Python, JavaScript
- **AI 모델**: YOLOv8
- **하드웨어 연동**: ROS, Arduino, Web Serial API
- **기타**: OpenCV, Requests, roslibpy

---

## 📦 설치 방법
### 🛠️ 설치 및 실행 방법
✅ 1. Python 환경 구성
Python 3.8 이상이 설치되어 있어야 해.
가상환경을 사용하는 걸 추천해!

bash
복사
편집
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
### 📦 2. 필요한 패키지 설치
bash
복사
편집
pip install -r requirements.txt
requirements.txt 없으면 아래처럼 직접 설치해도 돼:

bash
복사
편집
pip install ultralytics opencv-python roslibpy requests numpy
### 🎥 3. 카메라 연결 확인
USB 웹캠 또는 Jetbot 스트리밍(예: http://<ip>:8080/stream) 준비
장치가 카메라로 인식되는지 확인
### 🔌 4. 아두이노 연결
시리얼 방식 (crossing_gate.py):

Arduino 연결 후 포트 확인 (예: COM3, /dev/ttyUSB0)
HTTP 방식 (machine_gate.py):

Arduino가 웹서버로 동작해야 하고, IP 주소 확인 필요 (예: 192.168.137.134)
### 🚦 5. 파일 실행 방법
흉기 감지 및 경보 시스템 실행

bash
복사
편집
python machine_police.py
시리얼 게이트 제어 시스템 실행

bash
복사
편집
python crossing_gate.py
무선 게이트 제어 시스템 실행

bash
복사
편집
python machine_gate.py
실행 중 q 키를 누르면 카메라 창이 닫혀.

📢 전체 시스템은 ROS 기반의 자율 순찰, 택배 운송, 실시간 웹페이지 모니터링으로 확장되며, 본 레포는 그 중 보안 시스템의 핵심 처리 로직을 담당합니다.
