import cv2
import numpy as np

# 定義顏色範圍的上下界 (使用 BGR 顏色空間)
# 例如：紅色範圍
lower_b, lower_g, lower_r = 0, 0, 100
upper_b, upper_g, upper_r = 50, 50, 255

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
        
        # 顯示檢測到的顏色和位置
        print(f"檢測到顏色區域： x={x}, y={y}, w={w}, h={h}")

    # 顯示畫面和遮罩
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    # 按下q鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源並關閉視窗
cap.release()
cv2.destroyAllWindows()
