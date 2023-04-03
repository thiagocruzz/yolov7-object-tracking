import cv2

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, img = cap.read()

    qcd = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
    if retval:
        mg = cv2.polylines(img, points.astype(int), True, (0, 255, 0), 3)

        for s, p in zip(decoded_info, points):
            img = cv2.putText(img, s, p[0].astype(int),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('img', img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()   
cv2.destroyAllWindows()