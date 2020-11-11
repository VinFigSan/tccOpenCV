import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('classifier/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('classifier/haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    gray_face = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_frame = face_cascade.detectMultiScale(gray_face)
    for (x, y, w, h) in face_frame:
        gray_eye = gray_face[y: y+h, x: x+w]
        eye_frame = eye_cascade.detectMultiScale(gray_eye)
        cv2.imshow("Face", gray_eye)
        for (eye_x, eye_y, eye_w, eye_h) in eye_frame:
            gray_iris = gray_eye[eye_x: eye_x+eye_w, eye_y: eye_y+eye_h]
            #cv2.rectangle(frame, (x, y), (eye_x + eye_w, eye_y + eye_h), (255, 0, 0), 1)
            #cv2.putText(frame, "Olhos detectados", (eye_x, eye_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            _, gray_iris = cv2.threshold(gray_iris, 42, 255, cv2.THRESH_BINARY)
            cv2.imshow("Eyes", gray_iris)
    cv2.imshow("O todo", frame)
    key = cv2.waitKey(1) 
    if key == 27: #Tecla esc
        break

cap.release()
cv2.destroyAllWindows()

'''

#TODO: Fazer um melhoramento das capturas

def locate_eyes(frames, detector):
    eyes = detector.detectMultiScale(frames)
    width = np.size(frames, 1) 
    height = np.size(frames, 0)
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass
        eyecenter = x + w / 2  
        if eyecenter < width * 0.5:
            left_eye = frames[y:y + h, x:x + w]
        else:
            right_eye = frames[y:y + h, x:x + w]
    return left_eye, right_eye

detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)
#abertura da captura

        gray_frame = gray_face[y: y+h, x: x+w]
        eye_frame = locate_eyes(gray_frame, eye_cascade)
        #eye_frame = eye_cascade.detectMultiScale(gray_frame)
        for eye in eye_frame: #(ex, ey, ew, eh)
            #eye_selection = gray_frame[ey: ey+eh, ex:ex+eh]
            if eye is not None:
                _, eye = cv2.threshold(eye, 42, 255, cv2.THRESH_BINARY)
                eye = cv2.erode(eye, None, iterations=2)
                eye = cv2.dilate(eye, None, iterations=2)
                #eye = cv2.medianBlur(eye, 3)
                keypoints = detector.detect(eye)
                eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG)
                #print(eye.shape)
                eye = cv2.resize(eye, None, fx=5, fy=5)
                cv2.imshow("eye", eye)
'''