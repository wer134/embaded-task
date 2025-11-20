import cv2 as cv
import numpy as np
import threading, time
import SDCar

# --- 전역 변수 설정 ---
v_x = 320
v_y = 240

v_x_grid = [int(v_x * i / 10) for i in range(1, 10)] 

moment = np.array([0, 0, 0])
is_running = True
enable_linetracing = False
speed = 30  # 속도

# 자동차 객체 생성
car = SDCar.Drive()

# 1초마다 alive!!를 출력하여 프로그램이 동작 중임을 터미널에 표시
def func_thread():
    i = 0
    while True:
        print("alive!!")
        time.sleep(1)
        i += 1
        if is_running is False:
            break

# --- 영상 처리 함수 (HSV 변환) 
def detect_maskY_HSV(frame):
    crop_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    crop_hsv = cv.GaussianBlur(crop_hsv, (5, 5), cv.BORDER_DEFAULT)
    # 노란색 범위 (H: 25~35, S: 50~255, V: 100~255)
    mask_Y = cv.inRange(crop_hsv, (25, 50, 100), (35, 255, 255))
    return mask_Y

# --- 라인 트레이싱 주행 로직 
def line_tracing(cx):
    global v_x_grid
    
    # 노란선이 화면의 왼쪽 그리드(2~3) 사이에 위치해야 직진 (우측 통행)
    if v_x_grid[2] <= cx < v_x_grid[3]:
        car.motor_go(speed)
        print('go') # 제어화면 출력을 위한 로그
    elif cx <= v_x_grid[2]:
        car.motor_left(speed)
        print('turn left')
    elif cx >= v_x_grid[3]:
        car.motor_right(speed)
        print('turn right')
    else:
        car.motor_go(speed)
        print('go (exception)')

# --- 키 입력 처리 함수 
def key_cmd(which_key):
    global enable_linetracing, is_running
    is_exit = False
    
    print('which_key', which_key) 

    # 'q' 키: 프로그램 종료
    if which_key & 0xFF == ord('q'):
        car.motor_stop()
        print('exit')
        is_exit = True
        
    # 'e' 키: 라인 트레이싱 시작
    elif which_key & 0xFF == ord('e'):
        enable_linetracing = True
        print('enable_linetracing:', enable_linetracing)
        
    # 'w' 키: 라인 트레이싱 중지 및 정지
    elif which_key & 0xFF == ord('w'):
        enable_linetracing = False
        car.motor_stop()
        print('enable_linetracing:', enable_linetracing)
        
    return is_exit

# --- 메인 함수 ---
def main():
    global is_running, enable_linetracing
    
    # 카메라 설정
    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, v_x)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, v_y)

    # 스레드 시작 
    t_task1 = threading.Thread(target=func_thread)
    t_task1.start()

    try:
        while camera.isOpened():
            ret, frame = camera.read()
            if not ret:
                break
            
            frame = cv.flip(frame, -1) # 카메라 반전

            # --- Image Processing ---
            crop_img = frame[120:, :] # 하단부 자르기 (ROI)
            maskY = detect_maskY_HSV(crop_img)
            contours, _ = cv.findContours(maskY, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            cx = 0 # 초기값

            if len(contours) > 0:
                c = max(contours, key=cv.contourArea)
                m = cv.moments(c)
                
                if m['m00'] > 0:
                    cx = int(m['m10'] / m['m00'])
                    cy = int(m['m01'] / m['m00'])
                    
                    # 화면에 중심점과 외곽선 그리기
                    cv.circle(crop_img, (cx, cy), 3, (0, 0, 255), -1)
                    cv.drawContours(crop_img, contours, -1, (0, 255, 0), 3)
                    
                    # 라인 트레이싱 모드일 때 주행 함수 호출
                    if enable_linetracing:
                        line_tracing(cx)

            # 라인을 놓쳤거나 트레이싱 모드가 아니면 정지 (안전장치)
            if enable_linetracing and cx == 0:
                 pass # 필요시 car.motor_stop() 추가

            # 화면 출력
            cv.imshow('maskY', maskY)
            cv.imshow('crop_img', crop_img)

            # --- 키 입력 대기 및 처리 ---
            which_key = cv.waitKey(20)
            if which_key > 0:
                if key_cmd(which_key): # q가 입력되면 True 반환
                    break

    except Exception as e:
        print(e)
        
    finally:
        is_running = False # 스레드 종료 플래그
        car.clean_GPIO()
        cv.destroyAllWindows()
        camera.release()

if __name__ == '__main__':
    main()
