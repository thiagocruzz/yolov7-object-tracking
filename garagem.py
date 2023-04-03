import cv2
import numpy as np
from statistics import mean

areaGaragem = [258, 516, 379, 203,[1],"Garagem"]
areaFrente = [897, 566, 298, 154,[1],"Frente"]
areaRua = [1018, 105, 261, 252,[1],"Rua"]
areas = [areaGaragem,areaFrente,areaRua]

# cam1 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture('https://cameras.santoandre.sp.gov.br/coi04/ID_587')
#cam1 = cv2.VideoCapture('http://thiagocruzz.ddns-intelbras.com.br:81/stream')
cam2 = cv2.VideoCapture('rtsp://adminremoto:senha123@thiagocruzz.ddns-intelbras.com.br/:554/cam/realmonitor?channel=2&subtype=0')
cam3 = cv2.VideoCapture('rtsp://adminremoto:senha123@thiagocruzz.ddns-intelbras.com.br/:554/cam/realmonitor?channel=3&subtype=0')
cam4 = cv2.VideoCapture('rtsp://adminremoto:senha123@thiagocruzz.ddns-intelbras.com.br/:554/cam/realmonitor?channel=4&subtype=0')

def vconcat_resize(img_list, interpolation 
                   = cv2.INTER_CUBIC):
      # take minimum width
    w_min = min(img.shape[1] 
                for img in img_list)
      
    # resizing images
    im_list_resize = [cv2.resize(img,
                      (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                 interpolation = interpolation)
                      for img in img_list]
    # return final image
    return cv2.vconcat(im_list_resize)

while(cam1.isOpened() & cam2.isOpened() & cam3.isOpened() & cam4.isOpened()):
    retCam3, imgCam3 = cam3.read()
    retCam1, imgCam1 = cam1.read()
    retCam2, imgCam2 = cam2.read()
    retCam4, imgCam4 = cam4.read() 

    scale_percent = 50
    width = int(imgCam2.shape[1] * scale_percent / 100)
    height = int(imgCam2.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    imgResize1 = cv2.resize(imgCam1, dim, interpolation = cv2.INTER_AREA)
    imgResize2 = cv2.resize(imgCam2, dim, interpolation = cv2.INTER_AREA)
    imgResize3 = cv2.resize(imgCam3, dim, interpolation = cv2.INTER_AREA)
    imgResize4 = cv2.resize(imgCam4, dim, interpolation = cv2.INTER_AREA)

    p = cv2.hconcat([imgResize1, imgResize2])
    p2 = cv2.hconcat([imgResize3, imgResize4])
    img = vconcat_resize([p, p2])
    
    # r = cv2.selectROI("select the area", img, fromCenter=False)
    # print('Selected bounding boxes: {}'.format(r))
    # break

    imgCinza =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgCinza,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgBlur = cv2.medianBlur(imgTh,5)
    kernel = np.ones((3,3),np.int8)
    imgDil = cv2.dilate(imgBlur,kernel)
    for x,y,w,h,limite,label in areas:
        recorte = imgDil[y:y+h,x:x+w]
        qtdPxBranco = cv2.countNonZero(recorte)
        limite.insert(0,qtdPxBranco)
        media = round(mean(limite))

        cor =  (0,0,255) if qtdPxBranco > mean(limite)*1.25 else (0,255,0)
        corTexto =  (0,0,0) if qtdPxBranco > mean(limite)*1.25 else (0,0,0)
        
        if len(limite)>500:
            limite = limite[ : -1]

        cv2.rectangle(img,(x,y-20),(x+w,y-2),cor,-1)
        cv2.putText(img,label + " - Variacao " + str(round(qtdPxBranco/media*100,2)) + "%",(x+5,y-5),cv2.FONT_HERSHEY_PLAIN,1,corTexto,1)       
        cv2.rectangle(img,(x,y),(x+w,y+h),cor,2)
    
    cv2.imshow('Final', img)  
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cam1.release() 
cam2.release()   
cam3.release()   
cam4.release()   
cv2.destroyAllWindows()