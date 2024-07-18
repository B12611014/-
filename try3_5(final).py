import cv2
import mediapipe as mp
import math
import serial
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 根據兩點的座標，計算角度
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_

# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(finger_angle):
    if finger_angle is None:
        # 如果 finger_angle 是 None，可以返回一個預設值，或者直接返回 ''
        return ''
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if  f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        return '0'
    elif f1>=50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '1'
    elif f1>=50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '2'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5>50:
        return '3'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '4'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '5'
    elif f1<50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
        return '6'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '7'
    elif f1<50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '8'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5>=50:
        return '9'
    else:
        return '0'    #隨便預設的



cap = cv2.VideoCapture(0)  # 讀取攝影機
fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
lineType = cv2.LINE_AA  # 印出文字的邊框


# 開啟串口通信
serial_port = "/dev/cu.usbserial-1120"
arduino = serial.Serial(serial_port, 9600, timeout=1)

# 定義馬達動作狀態
MOTOR_STATE_IDLE = 0
MOTOR_STATE_ROTATE_90 = 1
MOTOR_STATE_ROTATE_180 = 2

motor_state = MOTOR_STATE_IDLE

# 定義計時器變數
start_time = time.time()

# mediapipe 啟用偵測手掌
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.9,
    #這個參數用於指定偵測物件時所需的最小信心度。信心度是指模型對於其偵測結果的自信程度，通常以概率的形式表示（例如0到1之間的值）。設置min_detection_confidence為0.9表示只有當模型對於偵測物件的信心度高於90%時，該物件才會被接受作為偵測結果。
    min_tracking_confidence=0.9
    #這個參數用於指定追蹤物件時所需的最小信心度。與偵測不同，追蹤是指在連續的幀中跟蹤已偵測到的物件。設置min_tracking_confidence為0.9表示只有當模型對於跟蹤物件的信心度高於90%時，該物件的追蹤才會被保持。
    ) as hands:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    w, h = 216, 125

    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (w, h))
        if not ret:
            print("Cannot receive frame")
            break
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img2) #將處理過的影象傳遞給 Hands 物件進行手部檢測，並獲取檢測結果。
        if results.multi_hand_landmarks:  #如果成功檢測到手部姿勢，則執行以下操作
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points = []
                for i in hand_landmarks.landmark:
                    x = i.x * w
                    y = i.y * h
                    finger_points.append((x, y))
                if finger_points:
                    finger_angle = hand_angle(finger_points)
                    text = hand_pos(finger_angle)
                    cv2.putText(img, text, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10,
                                cv2.LINE_AA)  # 文字大小為5，顏色為白色，粗細為10

                    # 判斷手勢為 "3" 時
                    if text == '3':
                        current_time = time.time() - start_time

                        if motor_state == MOTOR_STATE_IDLE and current_time > 5:
                            # 旋轉馬達到90度位置，停頓5秒
                            arduino.write(b'90')
                            print("Rotating to 90 degrees")
                            motor_state = MOTOR_STATE_ROTATE_90
                            start_time = time.time()

                        elif motor_state == MOTOR_STATE_ROTATE_90 and current_time > 10:
                            # 旋轉馬達到180度位置，停頓10秒
                            arduino.write(b'180')
                            print("Rotating to 180 degrees")
                            motor_state = MOTOR_STATE_ROTATE_180
                            start_time = time.time()

                        elif motor_state == MOTOR_STATE_ROTATE_180 and current_time > 5:
                            # 旋轉馬達回到0度位置，停頓5秒
                            arduino.write(b'0') #b'0' 是一個字節串（byte string），代表要發送給 Arduino 的數據。
                            print("Rotating to 0 degrees")
                            motor_state = MOTOR_STATE_IDLE
                            start_time = time.time()

        cv2.imshow('camera', img)
        if cv2.waitKey(5) == ord('q'):
            break

cap.release()
arduino.close()
cv2.destroyAllWindows()


