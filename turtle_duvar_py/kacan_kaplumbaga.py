import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class KacanKaplumbaga(Node):
    def __init__(self):
        super().__init__('kacan_kaplumbaga')
        
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.konum_dinle, 10)
        self.x = 5.5
        self.y = 5.5
        
        self.create_timer(1.0, self.log_yazdir)
        self.create_timer(0.1, self.tick)
        
        # BONUS: Parametre tanımlamaları (Dışarıdan değiştirilebilecek değerler)
        self.declare_parameter('ileri_hizi', 2.0)
        self.declare_parameter('donme_hizi', 1.5)
        self.declare_parameter('sinir_alt', 1.0)
        self.declare_parameter('sinir_ust', 10.0)

    def konum_dinle(self, msg):
        self.x = msg.x
        self.y = msg.y

    def log_yazdir(self):
        self.get_logger().info(f'Konum -> X: {self.x:.2f} | Y: {self.y:.2f}')

    def tick(self):
        # BONUS: Parametre değerlerini koda çekme
        hiz = self.get_parameter('ileri_hizi').get_parameter_value().double_value
        donus = self.get_parameter('donme_hizi').get_parameter_value().double_value
        alt = self.get_parameter('sinir_alt').get_parameter_value().double_value
        ust = self.get_parameter('sinir_ust').get_parameter_value().double_value

        msg = Twist()
        
        if self.x < alt or self.x > ust or self.y < alt or self.y > ust:
            msg.linear.x = 0.5 
            msg.angular.z = donus
        else:
            msg.linear.x = hiz
            msg.angular.z = 0.0
            
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(KacanKaplumbaga())
    rclpy.shutdown()

if __name__ == '__main__':
    main()