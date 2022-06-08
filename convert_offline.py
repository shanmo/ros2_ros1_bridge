from rosbags.rosbag1 import Reader
from rosbags.serde import deserialize_cdr, ros1_to_cdr

from rosbags.rosbag2 import Writer
from rosbags.serde import serialize_cdr
from rosbags.typesys.types import std_msgs__msg__String as String
from rosbags.typesys.types import builtin_interfaces__msg__Time as Time
from rosbags.typesys.types import sensor_msgs__msg__CompressedImage as CompressedImage
from rosbags.typesys.types import std_msgs__msg__Header as Header

image_msgs = []
lidar_msgs = []
tf_msgs = []
timestamps = []

ros1_bag_name = './data/ros1_demo.bag'
ros2_bag_name = './data/ros2_demo'

# create reader instance
with Reader(ros1_bag_name) as reader:
    # iterate over messages
    for connection, timestamp, rawdata in reader.messages():
        timestamps.append(timestamp)

        if connection.topic == '/fr_camera/color/image_raw_throttled/compressed':
            msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
            image_msgs.append(msg)
            print(f"compressed image {msg.header.frame_id}")

        if connection.topic == '/rslidar_points':
            msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
            lidar_msgs.append(msg)
            print(f"lidar {msg.header.frame_id}")

        if connection.topic == '/tf_static':
            msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
            tf_msgs.append(msg)

from pathlib import Path
import shutil

dirpath = Path(ros2_bag_name)
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)

# create writer instance and open for writing
with Writer(ros2_bag_name) as writer:
    # add new connection
    topic = '/image_compressed'
    msgtype = CompressedImage.__msgtype__
    connection = writer.add_connection(topic, msgtype, 'cdr', '')

    for timestamp, img in zip(timestamps, image_msgs):
        writer.write(
            connection,
            timestamp,
            serialize_cdr(img, msgtype),
        )