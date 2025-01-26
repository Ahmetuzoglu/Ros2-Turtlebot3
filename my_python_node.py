import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from math import sqrt
class MoveToGoal(Node):
    def __init__(self):
        super().__init__('move_to_goal')
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.goal_x = 10.0
        self.goal_y = 15.0
        self.current_x = 0.0
        self.current_y = 0.0
        self.distance_threshold = 0.1
        self.goal_reached = False
        self.timer = self.create_timer(0.1, self.move_turtlebot)
    def move_turtlebot(self):
        if not self.goal_reached:
            distance = sqrt((self.goal_x - self.current_x)**2 + (self.goal_y - self.current_y)**2)
            if distance < self.distance_threshold:
                self.get_logger().info("Hedefe ulasildi")
                self.stop_robot()
                self.goal_reached = True
                return
            velocity_msg = Twist()
            velocity_msg.linear.x = 0.2
            velocity_msg.angular.z = 0.0
            self.cmd_vel_pub.publish(velocity_msg)
            self.current_x += 0.2
            self.current_y += 0.2
    def stop_robot(self):
        stop_msg = Twist()
        self.cmd_vel_pub.publish(stop_msg)
def main(args=None):
    rclpy.init(args=args)
    node = MoveToGoal()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()

