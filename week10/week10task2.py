import cv2
import numpy as np
import os

# 결과를 저장할 폴더 생성
output_dir = "result_images"
os.makedirs(output_dir, exist_ok=True)

def detect_lines(image_path, output_path):
    """
    이미지에서 노란색 또는 흰색 선을 검출하여 마스킹된 이미지를 저장합니다.
    """
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"오류: {image_path} 파일을 읽을 수 없습니다.")
        return

    # 1. BGR to HSV 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2. 노란색 범위 정의 (HSV)
    # Hue(색상): 20-35 (OpenCV의 H 범위는 0-179)
    # Saturation(채도): 40-255 (어느 정도 색이 있어야 함)
    # Value(명도): 40-255 (어느 정도 밝아야 함)
    lower_yellow = np.array([20, 40, 40])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 3. 흰색 범위 정의 (HSV)
    # Hue: 0-179 (흰색은 색상이 없으므로 H는 중요하지 않음)
    # Saturation: 0-40 (채도가 매우 낮아야 함)
    # Value: 200-255 (명도가 매우 높아야 함)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([179, 40, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    # 4. 노란색 마스크와 흰색 마스크 합치기 (OR 연산)
    combined_mask = cv2.bitwise_or(mask_yellow, mask_white)

    # (선택적) 노이즈 제거: 모폴로지 연산 (열림/닫힘)
    # 작은 점(노이즈)을 제거하거나 끊어진 선을 연결할 때 유용합니다.
    kernel = np.ones((5, 5), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel) # 작은 노이즈 제거
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel) # 선 안의 구멍 메우기

    # 5. 원본 이미지에 마스크 적용 (선만 남기고 나머지는 검게)
    result = cv2.bitwise_and(frame, frame, mask=combined_mask)

    # 6. 결과 이미지 저장
    cv2.imwrite(output_path, result)
    print(f"처리 완료: {output_path}")

# --- 메인 실행 ---

# 첨부된 4장의 이미지 파일 이름을 가정합니다.
# (이 스크립트와 같은 폴더에 이미지 파일 4개가 있어야 합니다)
# 실제 파일 이름으로 변경해주세요.

image_files = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']

for img_file in image_files:
    # 원본 파일이 존재하는지 확인
    if os.path.exists(img_file):
        output_file_name = os.path.join(output_dir, "processed_" + os.path.basename(img_file))
        detect_lines(img_file, output_file_name)
    else:
        print(f"경고: {img_file} 파일을 찾을 수 없습니다. 건너뜁니다.")

print(f"\n모든 처리가 완료되었습니다. '{output_dir}' 폴더를 확인하세요.")
