# about 

- bridge ROS1 rosbag to be used for ROS2 package 

# setup 

```bash 
pip install --extra-index-url https://rospypi.github.io/simple/ rospy rosbag sensor_msgs geometry_msgs
```

# topics converted 

- sensor_msgs/CompressedImage
- sensor_msgs/PointCloud2
- tf2_msgs/TFMessage

output from `ros2 bag info ros2_demo/`
```bash 
(env_model) sean@nuc:~/workspace/ros2_ros1_bridge/data$ ros2 bag info ros2_demo/

Files:             ros2_demo.db3
Bag size:          382.0 MiB
Storage id:        sqlite3
Duration:          37.141s
Start:             Feb 23 2022 13:42:38.704 (1645594958.704)
End:               Feb 23 2022 13:43:15.846 (1645594995.846)
Messages:          4691
Topic information: Topic: /image_raw | Type: sensor_msgs/msg/Image | Count: 156 | Serialization Format: cdr
                   Topic: /lidar | Type: sensor_msgs/msg/PointCloud2 | Count: 369 | Serialization Format: cdr
                   Topic: /tf_static | Type: tf2_msgs/msg/TFMessage | Count: 1 | Serialization Format: cdr
                   Topic: /tf | Type: tf2_msgs/msg/TFMessage | Count: 4165 | Serialization Format: cdr
```
