from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2

# ref https://gist.github.com/awesomebytes/958a5ef9e63821a28dc05775840c34d9
class ImageTools(object):
    def __init__(self):
        self._cv_bridge = CvBridge()

    def convert_ros_compressed_to_cv2(self, compressed_msg):
        np_arr = np.fromstring(compressed_msg.data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    def convert_ros_compressed_msg_to_ros_msg(self, compressed_msg,
                                              encoding='rgb8'):
        cv2_img = self.convert_ros_compressed_to_cv2(compressed_msg)
        ros_img = self._cv_bridge.cv2_to_imgmsg(cv2_img, encoding=encoding)
        return ros_img

