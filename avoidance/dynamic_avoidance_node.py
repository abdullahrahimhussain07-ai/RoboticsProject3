import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class DynamicAvoidanceNode(Node):
    def __init__(self):
        super().__init__('dynamic_avoidance_node')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)
        self.safe_distance_threshold = 1.5
        self.max_speed = 0.5
        self.get_logger().info("Dynamic Avoidance Node initialized.")

    def scan_callback(self, msg):
        ranges = msg.ranges
        if not ranges:
            return
        center_indices = len(ranges) // 2
        front_ranges = ranges[center_indices - 15 : center_indices + 15]
        valid_ranges = [r for r in front_ranges if not math.isnan(r) and not math.isinf(r)]
        min_distance = min(valid_ranges) if valid_ranges else self.safe_distance_threshold
        
        twist = Twist()
        if min_distance < self.safe_distance_threshold:
            twist.linear.x = self.max_speed * math.tanh(min_distance)
        else:
            twist.linear.x = self.max_speed
            twist.angular.z = 0.0
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = DynamicAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
