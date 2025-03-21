# Smart Gate Control System 🚦🔒

이 프로젝트는 YOLO 객체 인식 모델과 Arduino, ROS, 웹 기술을 활용한 **지능형 게이트 제어 시스템**입니다. 특정 객체(예: 사람, 칼, 특정 캐릭터 등)를 인식하여 자동으로 차단기를 제어하거나 부저를 작동시키는 기능을 포함하고 있어요.

## 📁 구성 파일

### 1. `machine_police.py`
- **기능**: 칼(knife) 객체 감지 시 부저를 작동하고, 감지 결과를 ROS 토픽으로 전송함.
- **사용 모델**: `knife.pt`
- **기술 요소**: YOLOv8, ROS, HTTP 스트리밍

### 2. `crossing_gate.py`
- **기능**: YOLO로 특정 객체 감지 시, 아두이노 시리얼 통신으로 차단기를 자동 제어함.
- **사용 모델**: `nano5.pt`
- **통신 방식**: 시리얼 포트 (`COM3` 등)

### 3. `machine_gate.py`
- **기능**: 특정 객체 감지 시, 아두이노 웹서버에 HTTP 요청을 통해 차단기를 무선으로 제어함.
- **사용 모델**: `people.pt`
- **통신 방식**: HTTP (예: `http://192.168.137.134/gate_control?cmd=raise`)

### 4. `gate_control.js`
- **기능**: 웹 브라우저에서 아두이노와 시리얼 통신으로 차단기 명령 전송 (Raise/Lower)
- **기술 요소**: Web Serial API (HTTPS 환경 필요)

## 🧠 사용 모델 요약

| 모델 이름     | 역할               |
|--------------|--------------------|
| `knife.pt`   | 칼 감지            |
| `people.pt`  | 사람 형상 감지     |
| `nano5.pt`   | 특수 객체 감지     |

## 🛠️ 설치 및 실행

### 1. Python 패키지 설치
```bash
pip install ultralytics opencv-python roslibpy requests numpy
