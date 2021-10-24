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
        self.cam_distance_to_center = 0.0
        self.DEPTH_CEN_ROW = 240 #-> sudah di cek sebelumnya
        self.DEPTH_CEN_COL = 424
        self.CEN_ROW = 1280//2
        self.CEN_COL = 720//2
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
        color_topic = "/camera/color/image_raw"
        depth_topic = "/camera/depth/image_rect_raw"
        self.color_image_sub = rospy.Subscriber(color_topic, Image, self.color_image_callback)
        self.depth_image_sub = rospy.Subscriber(depth_topic, Image, self.depth_image_callback)

        rospy.loginfo("Waiting for image topics...")

    def color_image_callback(self, ros_image):
        font = cv.FONT_HERSHEY_SIMPLEX
  
        # org
        text_pos = (50, 50)
        
        # fontScale
        fontScale = 1
        
        # Blue color in BGR
        color = (255, 0, 0)
        
        # Line thickness of 2 px
        thickness = 2
        # print(type(ros_image))
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            # frame = self.bridge.imgmsg_to_cv(ros_image, "bgr8")
            # frame = self.bridge.imgmsg_to_cv2(ros_image, "passthrough")
            frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError as e:
            print(e)

        # Convert the image to a Numpy array since most cv2 functions
        # require Numpy arrays.
        frame = np.array(frame, dtype=np.uint8)
        msg = "cam distance to point in center: {0} m".format(self.cam_distance_to_center)
        frame = cv.putText(frame, msg,text_pos, font, fontScale, color, thickness, cv.LINE_AA)
        #set the center dot
        # col, row, _= frame.shape
        # print("row", row, "col", col)
        frame = cv.circle(frame, (self.CEN_ROW, self.CEN_COL), radius=2, color=(0, 0, 255), thickness=2)

        # Display the image.
        # cv2.imshow(self.node_name, frame)
        cv.imshow(self.node_name, frame)

        # Process any keyboard commands
        self.keystroke = cv.waitKey(5)
        if 32 <= self.keystroke and self.keystroke < 128:
            cc = chr(self.keystroke).lower()
            if cc == 'q':
                # The user has press the q key, so exit
                rospy.signal_shutdown("User hit q key to quit.")

    def depth_image_callback(self, ros_image):
        depth_data = self.bridge.imgmsg_to_cv2(ros_image, desired_encoding=ros_image.encoding)
        # ROW, COL = depth_data.shape
        # print((depth_data[self.ROW/2][self.COL/2])*0.001) #scaling mm to m
        self.cam_distance_to_center = depth_data[self.DEPTH_CEN_ROW][self.DEPTH_CEN_COL]*0.001
          

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