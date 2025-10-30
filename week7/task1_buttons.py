




import RPi.GPIO as GPIO
import time

# 핀 번호 및 이름 매칭
sw_pins = [5, 6, 13, 19]
sw_names = ["SW1", "SW2", "SW3", "SW4"]

# 클릭 횟수와 이전 상태 저장용 리스트
click_counts = [0, 0, 0, 0]
prev_sw_states = [0, 0, 0, 0]

# GPIO 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # BCM 모드 사용

# 4개 스위치 핀을 입력(IN)으로 설정, 풀다운 저항 활성화
for pin in sw_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("스위치 입력을 대기합니다. (Ctrl+C로 종료)")

try:
    while True:
        current_sw_states = [GPIO.input(pin) for pin in sw_pins]

        for i in range(len(sw_pins)):
            # 스위치가 떼어진 상태(0)에서 눌린 상태(1)로 변했는지 확인
            if current_sw_states[i] == 1 and prev_sw_states[i] == 0:
                click_counts[i] += 1

                print(f"('{sw_names[i]} click', {click_counts[i]})")
        
        prev_sw_states = current_sw_states[:]
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
