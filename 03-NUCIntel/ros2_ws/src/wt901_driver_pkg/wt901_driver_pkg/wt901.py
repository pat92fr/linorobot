import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Imu

from serial import Serial

class WT901BLECL(Node):


    def __init__(self):
        super().__init__('wt901_driver')
        self.publisher_ = self.create_publisher(Imu, '/imu', 10)
        timer_period = 0.02  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.myserial = Serial("/dev/ttyUSB1", baudrate = 115200, timeout = 1)
        self.myserial.reset_input_buffer()
        self.myserial.write([0xFF,0xAA,0x03,0x08,0x00]) # 50Hz
        self.myserial.write([0xFF,0xAA,0x00,0x00,0x00]) # SAVE
        
    def timer_callback(self):
        data = self.myserial.read(size=20)
        if not len(data) == 20:
            self.get_logger().info('Byte Error'+str(len(data)))
        elif( (data[0] == 0x55) and (data[1] == 0x61) ):

            #Acceleration
            self.accel_x = int.from_bytes(data[2:4], byteorder='little', signed="True")/32768.0*16
            self.accel_y = int.from_bytes(data[4:6], byteorder='little', signed="True")/32768.0*16
            self.accel_z = int.from_bytes(data[6:8], byteorder='little', signed="True")/32768.0*16

            #Angular velocity
            self.angular_velocity_x = int.from_bytes(data[8:10], byteorder='little', signed="True")/32768*2000
            self.angular_velocity_y = int.from_bytes(data[10:12], byteorder='little', signed="True")/32768*2000
            self.angular_velocity_z = int.from_bytes(data[12:14], byteorder='little', signed="True")/32768*2000

            #Angle
            self.angle_x = int.from_bytes(data[14:16], byteorder='little', signed="True")/32768*180
            self.angle_y = int.from_bytes(data[16:18], byteorder='little', signed="True")/32768*180
            self.angle_z = int.from_bytes(data[18:20], byteorder='little', signed="True")/32768*180

            msg = Imu()
            #msg.data = 'Hello World: %d' % self.i
            self.publisher_.publish(msg)

            #print(imu_sensor.getAngle())        
            #print(imu_sensor.getAccel())        
            #print(imu_sensor.getAngularVelocity())
        else:
            self.get_logger().info('Frame Error')

def main(args=None):
    rclpy.init(args=args)
    imu = WT901BLECL()
    rclpy.spin(imu)
    imu.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

