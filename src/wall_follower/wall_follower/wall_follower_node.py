import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallFollower(Node):
    def __init__(self):
        super().__init__('wall_follower')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscriber_ = self.create_subscription(LaserScan, '/scan', self.laser_callback, 10)
        self.get_logger().info('Wall Follower Node Started')

    def laser_callback(self, msg):
        twist = Twist()

        # Read ranges from LIDAR
        front = msg.ranges[0:15] + msg.ranges[-15:]      # front region
        right = msg.ranges[260:280]                      # right side (~270 degrees)
        left = msg.ranges[80:100]                        # left side (~90 degrees)

        # Filter out invalid readings (0.0)
        min_front = min([r for r in front if r > 0.1], default=10.0)
        min_right = min([r for r in right if r > 0.1], default=10.0)

        if min_front < 0.5:
            twist.linear.x = 0.0
            twist.angular.z = 0.5  # stop and turn left if obstacle in front
        elif min_right < 0.3:
            twist.linear.x = 0.2
            twist.angular.z = 0.2  # slow forward, turn slightly left
        elif min_right > 0.5:
            twist.linear.x = 0.2
            twist.angular.z = -0.2  # slow forward, turn slightly right
        else:
            twist.linear.x = 0.3
            twist.angular.z = 0.0  # go forward fast when clear

        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = WallFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

