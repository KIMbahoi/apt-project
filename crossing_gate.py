import cv2
import numpy as np
import time
import serial
from ultralytics import YOLO

# YOLO 모델 및 클래스 이름 설정
model = YOLO("./nano5.pt")
class_names = ['bunchiko', 'dragonite', 'garados', 'rosa', 'tree']

# 시리얼 포트 설정 (Windows의 경우 대문자로 작성)
arduino_port = 'COM3'  # 환경에 맞게 수정하세요.
baud_rate = 115200
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # 시리얼 연결 안정화 대기

# 디바운스(중복 전송 방지)를 위한 타이머 변수
last_command_time = 0
command_cooldown = 5  # 5초 동안 중복 전송 방지

# 모델 실행 주기를 10초로 설정
frame_interval = 10  # 10초마다 한 번만 실행
last_frame_time = time.time()  # 마지막 모델 실행 시간 기록

# 아두이노로부터 받은 메시지 처리 함수
def read_from_arduino():
    if ser.in_waiting > 0:  # 수신된 데이터가 있으면
        message = ser.readline().decode('utf-8').strip()  # 메시지를 읽고 디코딩
        print(message)

def detection_loop():
    global last_command_time, last_frame_time
    cap = cv2.VideoCapture(0)  # 웹캠 사용
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽어올 수 없습니다.")
            break

        # 10초마다 모델을 실행하도록 제어
        current_time = time.time()
        if current_time - last_frame_time >= frame_interval:  # 10초마다 실행
            # YOLO 모델로 객체 감지
            results = model(frame)

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls)
                    conf = float(box.conf)
                    if conf > 0.7:  # 신뢰도 임계치
                        label = f"{class_names[cls]} ({conf * 100:.1f}%)"
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        # 신뢰도가 0.9 이상이면, 일정 시간 이후에만 아두이노에 명령 전송
                        if conf > 0.9 and (time.time() - last_command_time) > command_cooldown:
                            print("객체 검출됨")
                            ser.write('RAISE\n'.encode())  # 아두이노에 차단기 올리기 명령 전송
                            print("차단바 올리기 명령 전송.")

                            ser.flush()  # 버퍼 비우기
                            last_command_time = time.time()

            # 마지막 모델 실행 시간 업데이트
            last_frame_time = current_time

        # 아두이노로부터 메시지 수신
        read_from_arduino()

        # 실시간 영상 출력
        cv2.imshow("YOLO Object Detection", frame)
        
        # 'q' 키를 눌러 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detection_loop()
    ser.close()  # 시리얼 포트 닫기
