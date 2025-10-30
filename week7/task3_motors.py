import RPi.GPIO as GPIO
import time

# Motor A (Left)
PWMA = 18
AIN1 = 22
AIN2 = 27

# Motor B (Right)
PWMB = 23
BIN1 = 25
BIN2 = 24

# Switches
SW1 = 5  # Forward
SW2 = 6  # Right
SW3 = 13 # Left
SW4 = 19 # Backward

# GPIO 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 모터 핀 6개 모두 출력(OUT)으로 설정
motor_pins = [PWMA, AIN1, AIN2, PWMB, BIN1, BIN2]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# 스위치 핀 4개 모두 입력(IN) 및 풀다운 저항 설정
switch_pins = [SW1, SW2, SW3, SW4]
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# PWM 객체 생성 (PIN, Freq)
L_Motor = GPIO.PWM(PWMA, 500) # 주파수 500Hz
R_Motor = GPIO.PWM(PWMB, 500)

# PWM 시작 (듀티 사이클 0 = 정지)
L_Motor.start(0)
R_Motor.start(0)

# 모터 속도 설정 함수
def set_motor_speed(motor, speed):
    motor.ChangeDutyCycle(speed) # 0 ~ 100

# 모터 방향 설정 함수 (1: 정방향, 0: 역방향, -1: 정지)
def set_motor_direction(pin1, pin2, direction):
    if direction == 1:      # 정방향 (AIN1=0, AIN2=1)
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 1) 
    elif direction == 0:    # 역방향 (AIN1=1, AIN2=0)
        GPIO.output(pin1, 1)
        GPIO.output(pin2, 0)
    else:                   # 정지 (AIN1=0, AIN2=0)
        GPIO.output(pin1, 0)
        GPIO.output(pin2, 0)

print("스위치로 자동차를 조종하세요. (Ctrl+C로 종료)")

try:
    while True:
        speed = 50 # 50% 속도로 설정 (과제 1번 내용)
        
        if GPIO.input(SW1) == 1: # SW1: 전진
            print("SW1: Forward") 
            set_motor_direction(AIN1, AIN2, 1) # 왼쪽 정방향
            set_motor_direction(BIN1, BIN2, 1) # 오른쪽 정방향
            set_motor_speed(L_Motor, speed)
            set_motor_speed(R_Motor, speed)
            
        elif GPIO.input(SW4) == 1: # SW4: 후진
            print("SW4: Backward") 
            set_motor_direction(AIN1, AIN2, 0) # 왼쪽 역방향
            set_motor_direction(BIN1, BIN2, 0) # 오른쪽 역방향
            set_motor_speed(L_Motor, speed)
            set_motor_speed(R_Motor, speed)
            
        elif GPIO.input(SW2) == 1: # SW2: 오른쪽 (왼쪽 정방향, 오른쪽 역방향)
            print("SW2: Right")
            set_motor_direction(AIN1, AIN2, 1)
            set_motor_direction(BIN1, BIN2, 0)
            set_motor_speed(L_Motor, speed)
            set_motor_speed(R_Motor, speed)
            
        elif GPIO.input(SW3) == 1: # SW3: 왼쪽 (왼쪽 역방향, 오른쪽 정방향)
            print("SW3: Left") 
            set_motor_direction(AIN1, AIN2, 0)
            set_motor_direction(BIN1, BIN2, 1)
            set_motor_speed(L_Motor, speed)
            set_motor_speed(R_Motor, speed)
            
        else: # 아무것도 눌리지 않으면 정지
            set_motor_speed(L_Motor, 0)
            set_motor_speed(R_Motor, 0)
        
        time.sleep(0.05) # 0.05초 간격으로 확인

except KeyboardInterrupt:
    print("\n작동 중지")
    pass

finally:
    L_Motor.stop()
    R_Motor.stop()
    GPIO.cleanup()
