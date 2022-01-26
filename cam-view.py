#!/usr/bin/env python3
'''
Created in 27 January 2022, since this is repetitive then may as well made this template to github
'''

import rospy
from cv_bridge import CvBridge, CvBridgeError
import cv2
import sensor_msgs.msg as sensor


def callback(data):
    Bridge = CvBridge()
    try:
        cv_img = Bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    
    cv2.imshow("image", cv_img)
    
    if(cv2.waitKey(1) == ord('q')):#i think 1 milisecond is good enough
        cv2.destroyAllWindows()

    

def main():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('uniCamView', anonymous=True)
    
    topic_name = "/zed2i/zed_node/stereo/image_rect_color/"
    rospy.Subscriber(topic_name, sensor.Image, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == "__main__":
    print("Ctrl+C to stop")
    main()
    

