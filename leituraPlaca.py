import cv2
import numpy as np
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cap = cv2.VideoCapture('video_nivus.MP4')
#cap = cv2.VideoCapture(0)
placas=[]

while(cap.isOpened()):
    ret, img = cap.read()
    if np.sum(img) == 0: break

    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)    
    desfoque = cv2.GaussianBlur(bin, (5, 5), 0)
    
    contornos, hierarquia = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        if perimetro > 200:
            aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            if len(aprox) == 4:
                (x, y, alt, lar) = cv2.boundingRect(c)
                if(lar>alt): break
                cv2.rectangle(img, (x, y), (x + alt, y + lar), (0, 255, 0), 2)
                # roi = img[y:y + lar, x:x + alt]               
                
                # roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                # roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
                # roi = cv2.bilateralFilter(roi,9,75,75)

                # imgBlur = cv2.medianBlur(roi,5)
                # kernel = np.ones((3,3),np.int8)
                # roi = cv2.dilate(roi,kernel)

                # config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'
                # date_pattern = '(?=(?:.*[0-9]){3})(?=(?:.*[A-Z]){4})([A-Z0-9]){6}([0-9])'
                # text = pytesseract.image_to_string(roi, config=config)

                # if re.match(date_pattern, text.strip()): 
                #     text=text.strip()
                #     if len(text)==7: 
                #         placas.append(text)            
                #         print(placas)

                cv2.imshow('img', img)
                #cv2.imshow('imgDesfoque', roi)   

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break