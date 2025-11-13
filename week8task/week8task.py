import RPi.GPIO as GPIO
import time
import serial  # 블루투스 시리얼 통신용 라이브러리
import threading # 시리얼 입력을 백그라운드에서 처리하기 위한 라이브러리

# --- 1. 모터 핀 설정 (이전과 동일) ---
# Motor A (Left)
PWMA = 18
AIN1 = 22
AIN2 = 27

# Motor B (Right)
PWMB = 23
BIN1 = 25
BIN2 = 24

# --- 2. 블루투스 시리얼 설정 ---
SERIAL_PORT = "/dev/ttyS0"  # 라즈베리파이3/4의 기본 시리얼 포트
BAUDRATE = 9600
ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=1)

# --- 3. GPIO 설정 (이전과 동일) ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

motor_pins = [PWMA, AIN1, AIN2, PWMB, BIN1, BIN2]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)
L_Motor.start(0)
R_Motor.start(0)

# --- 4. 모터 제어 함수 (이전과 동일) ---
def set_motor_speed(motor, speed):
    motor.ChangeDutyCycle(speed)

def set_motor_direction(pin1, pin2, direction):
    if direction == 1:      # 정방향
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 1)
    elif direction == 0:    # 역방향
        GPIO.output(pin1, 1)
        GPIO.output(pin2, 0)
    else:                   # 정지 (Brake)
        GPIO.output(pin1, 1) # 정지 시 0,0 대신 1,1을 주면 더 빨리 멈춥니다.
        GPIO.output(pin2, 1)

# --- 5. 명령(Command) 함수 구현 ---
speed = 50 # 기본 속도

def go():
    set_motor_direction(AIN1, AIN2, 1)
    set_motor_direction(BIN1, BIN2, 1)
    set_motor_speed(L_Motor, speed)
    set_motor_speed(R_Motor, speed)

def back():
    set_motor_direction(AIN1, AIN2, 0)
    set_motor_direction(BIN1, BIN2, 0)
    set_motor_speed(L_Motor, speed)
    set_motor_speed(R_Motor, speed)

def left():
    set_motor_direction(AIN1, AIN2, 0) # 왼쪽 역방향
    set_motor_direction(BIN1, BIN2, 1) # 오른쪽 정방향
    set_motor_speed(L_Motor, speed)
    set_motor_speed(R_Motor, speed)

def right():
    set_motor_direction(AIN1, AIN2, 1) # 왼쪽 정방향
    set_motor_direction(BIN1, BIN2, 0) # 오른쪽 역방향
    set_motor_speed(L_Motor, speed)
    set_motor_speed(R_Motor, speed)

def stop():
    set_motor_speed(L_Motor, 0)
    set_motor_speed(R_Motor, 0)
    #set_motor_direction(AIN1, AIN2, -1) # Brake
    #set_motor_direction(BIN1, BIN2, -1) # Brake

# --- 6. 시리얼 스레드 및 메인 루프 ---

gData = "" # 블루투스 명령어를 저장할 전역 변수

def serial_thread():
    global gData
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data: # 데이터가 있는 경우에만
                gData = data
                print(f"Received: {gData}")

# (요청사항) Main 함수 (루프)
def main():
    global gData
    print("Bluetooth Car Control Start... (Ctrl+C to stop)")
    try:
        while True:
            # gData 값에 따라 적절한 함수 호출
            if gData == "go":
                go()
                print("Action: GO")
            elif gData == "back":
                back()
                print("Action: BACK")
            elif gData == "left":
                left()
                print("Action: LEFT")
            elif gData == "right":
                right()
                print("Action: RIGHT")
            elif gData == "stop":
                stop()
                print("Action: STOP")
            

            
            time.sleep(0.05) # 0.05초 대기

    except KeyboardInterrupt:
        print("\nStopping...")
        pass
    finally:
        L_Motor.stop()
        R_Motor.stop()
        GPIO.cleanup()
        ser.close()
        print("Cleanup complete. Exiting.")

if __name__ == '__main__':
    # 시리얼 스레드를 시작 (daemon=True로 메인 프로그램 종료 시 자동 종료)
    t1 = threading.Thread(target=serial_thread, daemon=True)
    t1.start()
    
    main()