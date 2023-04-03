import cv2

cap = cv2.VideoCapture('rtsp://adminremoto:senha123@thiagocruzz.ddns-intelbras.com.br/:554/cam/realmonitor?channel=2&subtype=0')
#cap = cv2.VideoCapture('rtsp://adminremoto:senha123@192.168.15.36/:554/cam/realmonitor?channel=2&subtype=0')
#cap = cv2.VideoCapture(0)

print('abrindo camera')
while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
print('camera fechada')

cap.release()   
cv2.destroyAllWindows()
