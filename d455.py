#!/usr/bin/env python
import rospy                        #add ros for python
import cv2 as cv                    #add open cv library
from PIL import Image as pilIm      #add PIL library
import sensor_msgs.msg as sensor
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

frame = 0

def commented_cb(data):
   # global frame
   # # print("tipe data data:" + str(type(data.data))) <- is astring
   # bit = 921600
   # imArray = []
   # # count = 0
   # # id = 0
   # for i in data.data:
   #    imArray.append(ord(i))
   #    # count+=1
   #    # id+=1*(count % bit == 0)

   # im2d = np.reshape(imArray, (-1, 2))
   # # img = np.array(imArray)
   # saved = pilIm.fromarray((im2d * 255).astype(np.uint8))
   # name = str(frame)
   # name +=".png"
   # frame+=1
   # saved.save(name)
   # print(img)
   # print("------------------")
   # print(imArray)
   # print("-------------")
   # print(saved)

   # img[:,:,0] = numpy.ones([5,5])*64/255.0
   # img[:,:,1] = numpy.ones([5,5])*128/255.0
   # img[:,:,2] = numpy.ones([5,5])*192/255.0
   # print("tipe array:" + str(type(img)))
   # print(img)
   # im = pilIm.fromarray(array)
   #    print("showing image")
   #    img = cv.imread('/home/avinlnx/raspi_teleop/src/mengrealopencipi/src/index.jpeg', cv.IMREAD_GRAYSCALE)
   #    cv.imshow("image", img)
   # print(img)
   # print(len(img))
   a = 1

def callback(data):
    Cipibrij = CvBridge()
    try:
      cv_image = Cipibrij.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    cv.imshow("Image window", cv_image)
    cv.waitKey(3)
    print("done")

def main():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('peeker', anonymous=True)

    rospy.Subscriber("/camera/color/image_raw", sensor.Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    main()
    cv.destroyAllWindows()