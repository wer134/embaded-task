import cv2

# 1. Haar Cascade 분류기 로드
# XML 파일이 코드와 동일한 폴더에 있다고 가정합니다.
face_cascade_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)

if face_cascade.empty():
    print(f"오류: {face_cascade_path} 파일을 로드할 수 없습니다.")
    print("OpenCV GitHub에서 파일을 다운로드하여 이 스크립트와 동일한 폴더에 넣어주세요.")
    exit()

# 2. 카메라 캡처 객체 생성
# 0은 시스템의 기본 카메라를 의미합니다. (라즈베리파이 카메라 또는 USB 웹캠)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("오류: 카메라를 열 수 없습니다.")
    exit()

print("얼굴 검출 시작. 'q' 키를 누르면 종료됩니다.")

while True:
    # 3. 프레임 단위로 영상 읽기
    ret, frame = cap.read()
    if not ret:
        print("오류: 프레임을 읽을 수 없습니다.")
        break
    frame = cv2.flip(frame, -1)

    # 4. 얼굴 검출을 위해 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 5. 얼굴 검출 수행
    # detectMultiScale(image, scaleFactor, minNeighbors)
    # scaleFactor: 이미지 피라미드에서 사용할 축소 비율
    # minNeighbors: 얼굴로 감지하기 위한 최소 이웃 사각형 수 (값이 높을수록 정확도 UP, 탐지율 DOWN)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # 6. 검출된 얼굴 주위에 사각형 그리기
    for (x, y, w, h) in faces:
        # (원본 이미지, 시작점, 끝점, 색상(BGR), 두께)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 7. 결과 영상 출력
    cv2.imshow('Real-time Face Detection', frame)

    # 8. 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 9. 자원 해제
cap.release()
cv2.destroyAllWindows()
