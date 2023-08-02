import os
import cv2
import mediapipe as mp
import math
import datetime ,time

ssFolderName = 'screenshots'
if not os.path.exists(ssFolderName):
    os.makedirs(ssFolderName)
currentDir = os.getcwd()

enhancedImage = None
fontThickness = 2
didHandOpen = True
isTakingPicture = False
debugger = False

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cv2.namedWindow("Hand-tacking Test Application", cv2.WINDOW_KEEPRATIO)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)


def getDistance(a_x, a_y, b_x, b_y):
    dist = math.pow(a_x - b_x, 2) + math.pow(a_y - b_y, 2)
    return math.sqrt(dist)

def isFingerANearFingerB(_p1, _p2, _dist):
    distance = getDistance(_p1.x, _p1.y, _p2.x, _p2.y)
    return distance < _dist

while True:
    success, img = cap.read()
    if not success:
        print("Cannot capture frame. Exiting...")
        break
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, mpDraw.DrawingSpec(color=(255, 186, 84), thickness=10, circle_radius=1), mpDraw.DrawingSpec(color=(255, 255, 255), thickness=fontThickness))
            # Brigthness and Contrast adjustments
            enhanced_image = cv2.convertScaleAbs(img, alpha=1, beta=0)

            # Scales the window
            new_width = 1280
            new_height = 720
            enhancedImage = cv2.resize(enhanced_image, (new_width, new_height))
            
            # Detect if finger's are fully extended
            _right = handLms.landmark[mpHands.HandLandmark.THUMB_TIP].x < handLms.landmark[mpHands.HandLandmark.PINKY_TIP].x
            if _right:
                thumbExtended = handLms.landmark[mpHands.HandLandmark.THUMB_TIP].x < handLms.landmark[mpHands.HandLandmark.THUMB_IP].x
                indexExtended = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y < handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_PIP].y
                middleExtended = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP].y < handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_PIP].y
                ringExtended = handLms.landmark[mpHands.HandLandmark.RING_FINGER_TIP].y < handLms.landmark[mpHands.HandLandmark.RING_FINGER_PIP].y
                pinkyExtended = handLms.landmark[mpHands.HandLandmark.PINKY_TIP].y < handLms.landmark[mpHands.HandLandmark.PINKY_PIP].y
            else:
                thumbExtended = handLms.landmark[mpHands.HandLandmark.THUMB_TIP].x > handLms.landmark[mpHands.HandLandmark.THUMB_IP].x
                indexExtended = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y > handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_PIP].y
                middleExtended = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP].y > handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_PIP].y
                ringExtended = handLms.landmark[mpHands.HandLandmark.RING_FINGER_TIP].y > handLms.landmark[mpHands.HandLandmark.RING_FINGER_PIP].y
                pinkyExtended = handLms.landmark[mpHands.HandLandmark.PINKY_TIP].y > handLms.landmark[mpHands.HandLandmark.PINKY_PIP].y

            
            # Check for gestures
            if thumbExtended and not indexExtended and not middleExtended and not ringExtended and not pinkyExtended:
                cv2.putText(enhancedImage, "Thumbs Up", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), fontThickness)
            elif not thumbExtended and indexExtended and not middleExtended and not ringExtended and not pinkyExtended:
                cv2.putText(enhancedImage, "Pointing Finger", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), fontThickness)
            elif not thumbExtended and indexExtended and middleExtended and not ringExtended and not pinkyExtended:
                cv2.putText(enhancedImage, "Victory", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), fontThickness)
            elif thumbExtended and indexExtended and not middleExtended and not ringExtended and pinkyExtended and not isFingerANearFingerB(handLms.landmark[4], handLms.landmark[12], 0.1) and not isFingerANearFingerB(handLms.landmark[4], handLms.landmark[16], 0.1):
                cv2.putText(enhancedImage, "Spiderman", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), fontThickness)
            elif not thumbExtended and indexExtended and not middleExtended and not ringExtended and pinkyExtended and not isFingerANearFingerB(handLms.landmark[4], handLms.landmark[12], 0.1) and not isFingerANearFingerB(handLms.landmark[4], handLms.landmark[16], 0.1):
                cv2.putText(enhancedImage, "RockNRoll", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), fontThickness)
            elif not thumbExtended and indexExtended and not middleExtended and  not ringExtended and pinkyExtended and isFingerANearFingerB(handLms.landmark[4], handLms.landmark[12], 0.1) and isFingerANearFingerB(handLms.landmark[4], handLms.landmark[16], 0.1):
                cv2.putText(enhancedImage, "cCc", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), fontThickness)
            elif thumbExtended and indexExtended and middleExtended and ringExtended and pinkyExtended:
                if didHandOpen:
                    isTakingPicture = True
                    start_time = time.time()
                didHandOpen = False
                cv2.putText(enhancedImage, "Open Hand", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), fontThickness)
            elif not thumbExtended and not indexExtended and not middleExtended and not ringExtended and not pinkyExtended:
                if isTakingPicture:
                    end_time = time.time()
                    if end_time - start_time <= 2:  # Check if hand closed within 2 seconds
                        date = time.strftime("%Y %b %a  %H.%M.%S")
                        ssFileName = f"screenshot-{date}.jpg"
                        filePath = os.path.join(ssFolderName, ssFileName)
                        cv2.imwrite(filePath, enhancedImage)
                        isTakingPicture = False
                didHandOpen = True
                cv2.putText(enhancedImage, "First/Closed Hand", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), fontThickness)
            elif thumbExtended and not indexExtended and middleExtended and ringExtended and pinkyExtended and isFingerANearFingerB(handLms.landmark[4], handLms.landmark[8], 0.1):
                cv2.putText(enhancedImage, "OK", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), fontThickness)                
            else:
                cv2.putText(enhancedImage, "Unknown Gesture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), fontThickness)

            if debugger:                    
                print("Thumb Extended:", thumbExtended)
                print("Index Extended:", indexExtended)
                print("Middle Extended:", middleExtended)
                print("Ring Extended:", ringExtended)
                print("Pinky Extended:", pinkyExtended)
                print("--------------------")
                debugger = not debugger
    else:
        cv2.putText(enhancedImage, "No hand detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), fontThickness)
    
    if enhancedImage is not None and enhancedImage.shape[0] > 0 and enhancedImage.shape[1] > 0:
        cv2.imshow("Hand-tacking Test Application", enhancedImage)
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('z'):
        debugger = not debugger

cap.release()
cv2.destroyAllWindows()