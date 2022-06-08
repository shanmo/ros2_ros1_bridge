# for ros1
import rospy
from sensor_msgs.msg import CompressedImage
# for ros2
# cannot import due to ImportError: cannot import name 'Log' from 'rosgraph_msgs.msg'
# import rclpy

def image_callback(data):
    rospy.loginfo("subscribed to compressed image: %s", data.header.frame_id)

def main():
    rospy.init_node('ros1_listener', anonymous=True)
    rospy.Subscriber("/fr_camera/color/image_raw_throttled/compressed", CompressedImage, image_callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass