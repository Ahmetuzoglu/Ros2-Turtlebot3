import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import sqrt
class MoveToGoal(Node):
    def __init__(self):
        super().__init__('move_to_goal')
        self.odom_subscription = self.create_subscription(
            Odometry,
            '/odom',  
            self.odom_callback,
            10
        )       
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.goal_x = 2.0
        self.goal_y = -0.5
        self.current_x = 0.0
        self.current_y = 0.0
        self.distance_threshold = 0.05  
        self.goal_reached = False
        self.timer = self.create_timer(0.1, self.move_turtlebot)
    def odom_callback(self, msg):
        position = msg.pose.pose.position
        self.current_x = position.x
        self.current_y = position.y
        if not self.goal_reached:
            self.get_logger().info(f"Mevcut Konum: X: {self.current_x}, Y: {self.current_y}")          
    def move_turtlebot(self):
        if not self.goal_reached:
            distance = sqrt((self.goal_x - self.current_x)**2 + (self.goal_y - self.current_y)**2)
            if distance < self.distance_threshold:
                self.get_logger().info("Hedefe ulasildi")
                self.stop_robot()
                self.goal_reached = True
                return
            velocity_msg = Twist()
            max_linear_speed = 0.5  
            min_linear_speed = 0.05  
            velocity_msg.linear.x = max(min_linear_speed, min(max_linear_speed, distance))
            self.cmd_vel_pub.publish(velocity_msg)
            max_linear_speed = 0.5  
            min_linear_speed = 0.05  
            velocity_msg.linear.y = max(min_linear_speed, min(max_linear_speed, distance))
    def stop_robot(self):
        stop_msg = Twist()
        self.cmd_vel_pub.publish(stop_msg)
        stop_msg.linear.x = 0.0  
        stop_msg.angular.z = 0.0  
        stop_msg.linear.y = 0.0
        self.cmd_vel_pub.publish(stop_msg)
def main(args=None):
    rclpy.init(args=args)
    node = MoveToGoal()
    rclpy.spin(node)
    rclpy.shutdown()
    sys.exit()
if __name__ == '__main__':
    main()

