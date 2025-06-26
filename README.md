# Wall Follower Robot (ROS 2)

A simple reactive wall follower using LIDAR and TurtleBot3 in Gazebo simulation.

## Features
- Subscribes to `/scan`
- Publishes to `/cmd_vel`
- Avoids obstacles and follows right wall
- Works without map (pure reactive)

## How to Run

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 run wall_follower wall_follower_node
