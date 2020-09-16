import cv2
import numpy as np

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


#nominações
face_cascade = cv2.CascadeClassifier('classifier/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('classifier/haarcascade_eye.xml')
detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)
#abertura da captura
cap = cv2.VideoCapture(0)

#cv2.putText(frame,"Funfando",(30,100),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0))
while True:
    #inicio da leitura
    _, frame = cap.read()
    gray_face = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #identificação face e demonstração
    face_frame = face_cascade.detectMultiScale(gray_face)
    for (x, y, w, h) in face_frame: 
        gray_frame = gray_face[y: y+h, x: x+w]
        eye_frame = locate_eyes(gray_frame, eye_cascade)
        #identificação olhos e demonstração (a minha turminha complicada)
        #eye_frame = eye_cascade.detectMultiScale(gray_frame)
        for eye in eye_frame: #(ex, ey, ew, eh)
            #eye_selection = gray_frame[ey: ey+eh, ex:ex+eh]
            if eye is not None:
                _, eye = cv2.threshold(eye, 42, 255, cv2.THRESH_BINARY)
                """eye = cv2.erode(eye, None, iterations=2)
                eye = cv2.dilate(eye, None, iterations=4)
                eye = cv2.medianBlur(eye, 5)
                keypoints = detector.detect(eye)"""
                cv2.drawKeypoints(eye, keypoints, frame, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                cv2.imshow("eye", eye)
    
    
    #exibição e cancelamento
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27: #Tecle esc
        break

cap.release()
cv2.destroyAllWindows()