from rosbags.rosbag1 import Reader
from rosbags.serde import deserialize_cdr, ros1_to_cdr

from rosbags.rosbag2 import Writer
from rosbags.serde import serialize_cdr
from rosbags.typesys.types import sensor_msgs__msg__CompressedImage as CompressedImage
from rosbags.typesys.types import sensor_msgs__msg__PointCloud2 as pt2
from rosbags.typesys.types import tf2_msgs__msg__TFMessage as tf_m

from pathlib import Path
import shutil

def read_topic(ros1_bag_name, topic_name):
    results = []
    # create reader instance
    with Reader(ros1_bag_name) as reader:
        # iterate over messages
        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == topic_name:
                msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
                results.append((timestamp, msg))
                # print(f"read {msg.header.frame_id}")
    return results

if __name__ == "__main__":
    ros1_bag_name = './data/ros1_demo.bag'
    ros2_bag_name = './data/ros2_demo'

    dirpath = Path(ros2_bag_name)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    topic_name = "/fr_camera/color/image_raw_throttled/compressed"
    img_msgs = read_topic(ros1_bag_name, topic_name)

    topic_name = "/rslidar_points"
    lidar_msgs = read_topic(ros1_bag_name, topic_name)

    topic_name = "/tf_static"
    tf_msgs = read_topic(ros1_bag_name, topic_name)

    # create writer instance and open for writing
    with Writer(ros2_bag_name) as writer:
        # add new connection
        topic_name = "/image_compressed"
        img_msgtype = CompressedImage.__msgtype__
        img_conn = writer.add_connection(topic_name, img_msgtype, 'cdr', '')
        for timestamp, msg in img_msgs:
            writer.write(
                img_conn,
                timestamp,
                serialize_cdr(msg, img_msgtype),
            )

        # add new connection
        topic_name = "/lidar"
        ld_msgtype = pt2.__msgtype__
        ld_conn = writer.add_connection(topic_name, ld_msgtype, 'cdr', '')
        for timestamp, msg in lidar_msgs:
            writer.write(
                ld_conn,
                timestamp,
                serialize_cdr(msg, ld_msgtype),
            )

        # add new connection
        topic_name = "/tf"
        tf_msgtype = tf_m.__msgtype__
        tf_conn = writer.add_connection(topic_name, tf_msgtype, 'cdr', '')
        for timestamp, msg in tf_msgs:
            writer.write(
                tf_conn,
                timestamp,
                serialize_cdr(msg, tf_msgtype),
            )