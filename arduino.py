import cv2
import mediapipe as mp
import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

def sendData(data):
    data += "\n"
    print(data, end='')
    ser.write(data.encode())

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    data = [0,0]
    diff = 0

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            i = 0
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                if id == 4 or id == 8:
                	cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
               		if id == 4:
               			data[0] = (cx, cy)
               		if id == 8:
               			data[1] = (cx, cy)


            #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        diff = int((abs(data[0][1] - data[1][1])/400)*180)
        centery = int(abs(data[0][1] + data[1][1])/2)
        centerx = int(abs(data[0][0] + data[1][0])/2)
        string = "Angle: " + str(diff)
        cv2.putText(img, string, (centerx, centery), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.line(img, (data[0][0], data[0][1]), (data[1][0], data[1][1]), (255, 255, 255), 1)

        sendData(str(diff))

    # cTime = time.time()
    #
    # fps = 1 / (cTime - pTime)
    # pTime = cTime

    #cv2.putText(img, diff, (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
     #           (255, 0, 255), 3)

    cv2.imshow("Image", img)
    #cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
