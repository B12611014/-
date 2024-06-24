import cv2
import numpy as np

def nothing(x):
    pass

# 創建一個窗口
cv2.namedWindow('Trackbars')

# 在窗口中創建6個滑桿來調整RGB顏色範圍
cv2.createTrackbar('LowerR', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('LowerG', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('LowerB', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('UpperR', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('UpperG', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('UpperB', 'Trackbars', 255, 255, nothing)

# 開啟相機
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("無法讀取鏡頭!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("無法獲取畫面")
        break

    # 獲取滑桿當前位置
    lower_r = cv2.getTrackbarPos('LowerR', 'Trackbars')
    lower_g = cv2.getTrackbarPos('LowerG', 'Trackbars')
    lower_b = cv2.getTrackbarPos('LowerB', 'Trackbars')
    upper_r = cv2.getTrackbarPos('UpperR', 'Trackbars')
    upper_g = cv2.getTrackbarPos('UpperG', 'Trackbars')
    upper_b = cv2.getTrackbarPos('UpperB', 'Trackbars')

    # 定義顏色範圍
    lower_color = np.array([lower_b, lower_g, lower_r])
    upper_color = np.array([upper_b, upper_g, upper_r])

    # 過濾出指定顏色範圍內的部分
    mask = cv2.inRange(frame, lower_color, upper_color)

    # 找到顏色範圍內的輪廓
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 計算輪廓的邊界框
        x, y, w, h = cv2.boundingRect(contour)
        # 繪製邊界框
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 顯示畫面和遮罩
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    # 按下q鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源並關閉視窗
cap.release()
cv2.destroyAllWindows()
