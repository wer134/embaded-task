import RPi.GPIO as GPIO
import time

# 부저 핀
BUZZER = 12

# 스위치 핀
sw_pins = [5, 6, 13, 19]

# 도(4옥타브), 미, 솔, 시
notes = [262, 330, 392, 494] 

# GPIO 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

# 스위치 핀 설정 (입력, 풀다운)
for pin in sw_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# PWM 객체 생성 (PIN, Freq)
p = GPIO.PWM(BUZZER, 100) 

print("스위치 피아노 (Ctrl+C로 종료)")

note_playing = False # 현재 음이 연주 중인지 확인

try:
    while True:
        freq_to_play = 0
        
        # 4개 스위치를 확인하여 눌린 스위치의 음계를 찾음
        for i in range(len(sw_pins)):
            if GPIO.input(sw_pins[i]) == 1:
                freq_to_play = notes[i]
                break # 첫 번째로 눌린 스위치의 음만 연주
        
        if freq_to_play > 0:
            # 연주할 음이 있다면
            p.ChangeFrequency(freq_to_play) # 주파수 변경 
            if not note_playing:
                p.start(50) # 소리가 나고 있지 않았다면 50% 듀티 사이클로 시작 
                note_playing = True
        else:
            # 아무 스위치도 눌리지 않았다면
            if note_playing:
                p.stop() # 소리 끄기 
                note_playing = False
                
        time.sleep(0.01) # 빠른 반응을 위해 짧게 대기

except KeyboardInterrupt:
    pass

finally:
    p.stop()
    GPIO.cleanup()
