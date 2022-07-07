import qrcode_detect
import cv2
import pyrealsense2
from realsense_depth import *
def spinAroundLeft(speed = 1, angle = 1) :
    pass
def spinAroundLeft(speed = 1, angle = 1) :
    pass
def runForward(speed = 1):
    pass
def runBackward(speed = 1):
    pass
def turnRight(speed = 1):
    pass
def turnLeft(speed = 1):
    pass

def runToQrcode(x_center ,y_center, x_0, y_0, ACC = 0.9):
    
    if (1- abs(x_center - x_0)/x_0) <= ACC and x_center - x_0 <0 :
        turnLeft(1)
    elif (1- abs(x_center - x_0)/x_0) <= ACC and x_center - x_0 >0 :
        turnRight(1)
    else:
        runForward(1)
        
if __name__ == "__main__":
    # cap = cv2.VideoCapture(0)
    dc = DepthCamera()
    net, classes = qrcode_detect.loadWeight(weights = "./yolov4-tiny-custom_best.weights",cfg ="./yolov4-tiny.cfg",class_name = "./obj.names")
    checkRunToQR = True
    
    while checkRunToQR:
        # ret, color_frame = cap.read()
        ret, depth_frame, color_frame = dc.get_frame()
        image, indices, boxes, class_ids, confidences = qrcode_detect.detect(color_frame, net)
        height, width = image.shape[:2]
        cof = 0
        old_cof = 0
        distance = "NaN"
        for i in indices:
            i = i[0]
            cof = confidences[i]
            if cof >= old_cof:
                box = boxes[i]
                x = box[0]
                y = box[1]
                w = box[2]
                h = box[3]
            old_cof = cof
        image = qrcode_detect.drawImage(image, indices, boxes, class_ids, confidences, classes)

        if len(indices) > 0:
            runToQrcode(x+w/2, y+h/2, width/2, height/2)
            distance = depth_frame[int(x+w/2), int(y+h/2)]
            if int(distance) < 50:
                checkRunToQR = False        
        cv2.putText(image, "z: " + str(distance)+" mm", (20,80 ), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 1)
        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    # cap.release()
    cv2.destroyAllWindows()
