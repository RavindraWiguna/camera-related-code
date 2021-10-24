#!/usr/bin/env python
#got from https://answers.ros.org/question/304777/new-in-ros-sensor_msgsimage-in-opencv/
# import roslib; roslib.load_manifest('rbx1_vision')
import rospy
import sys
import cv2 as cv
# import cv2.cv as cv
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class cvBridgeDemo():
    def __init__(self):
        self.node_name = "cv_bridge_demo"

        rospy.init_node(self.node_name)

        # What we do during shutdown
        rospy.on_shutdown(self.cleanup)

        # Create the OpenCV display window for the RGB image
        self.cv_window_name = self.node_name
        # cv.NamedWindow(self.cv_window_name, cv.CV_WINDOW_NORMAL)
        # cv.MoveWindow(self.cv_window_name, 25, 75)

        # Create the cv_bridge object
        self.bridge = CvBridge()

        # Subscribe to the camera image and depth topics and set
        # the appropriate callbacks
        # topic_ = "/camera/color/image_raw"
        topic_ = "/camera/depth/image_rect_raw/"
        self.image_sub = rospy.Subscriber(topic_, Image, self.image_callback)

        rospy.loginfo("Waiting for image topics...")

    def image_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            # print(type(ros_image))
            # frame = self.bridge.imgmsg_to_cv(ros_image, "bgr8")
            # frame = self.bridge.imgmsg_to_cv2(ros_image, desired_encoding="passthrough")#pass thourgh bikin encodingnya jadi sama..., 
            frame = self.bridge.imgmsg_to_cv2(ros_image, desired_encoding=ros_image.encoding) #i think ini sama dengan passthrough, but better karena langsng?
            # frame = self.bridge.imgmsg_to_cv2(ros_image, desired_encoding="mono16")<- didnt wek, cause 16UC1 (encoding depth is 16 bit 1 layer/channel)
            # print(ros_image.encoding)

        except CvBridgeError as e:
            print(e)

        # Convert the image to a Numpy array since most cv2 functions
        # require Numpy arrays.
        frame = np.array(frame, dtype=np.uint16)*0.0001 #kalo 1/1000 itu warnanya kebnyakan putuh, jadi tak kali 1/10000 -> nevermind 1/1000 is the scaling (mm to m)
        # print(frame.shape) -> 480, 848
        # Display the image.
        # cv2.imshow(self.node_name, frame)
        cv.imshow(self.node_name, frame)
        ROW, COL = frame.shape
        print((frame[ROW/2][COL/2])*10)

        # Process any keyboard commands
        self.keystroke = cv.waitKey(5)
        if 32 <= self.keystroke and self.keystroke < 128:
            cc = chr(self.keystroke).lower()
            if cc == 'q':
                # The user has press the q key, so exit
                rospy.signal_shutdown("User hit q key to quit.")

    def cleanup(self):
        print("Shutting down vision node.")
        # cv2.destroyAllWindows() 
        cv.destroyAllWindows()  

def main(args):       
    try:
        cvBridgeDemo()
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down vision node.")
        cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)