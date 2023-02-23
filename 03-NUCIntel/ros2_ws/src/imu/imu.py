from serial import Serial

class WT901BLECL:
    def __init__(self, Port):
        self.myserial = Serial(Port, baudrate = 115200, timeout = 1)
        self.myserial.reset_input_buffer()
        self.accel_x = 0.
        self.accel_y = 0.
        self.accel_z = 0.
        self.angular_velocity_x = 0.
        self.angular_velocity_y = 0.
        self.angular_velocity_z = 0.
        self.angle_x = 0.
        self.angle_y = 0.
        self.angle_z = 0.

    def read(self):
        data = self.myserial.read(size=20)
        if not len(data) == 20:
            print('byte error:', len(data))

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

        else:
            print('frame error:')

    def getAngle(self):
        return (self.angle_x, self.angle_y, self.angle_z)

    def getAccel(self):
        return (self.accel_x, self.accel_y, self.accel_z)

    def getAngularVelocity(self):
        return (self.angular_velocity_x, self.angular_velocity_y, self.angular_velocity_z)

if __name__ == "__main__":

    imu_sensor =  WT901BLECL("COM6")
    while True:
        imu_sensor.read()
        print(imu_sensor.getAngle())        
        #print(imu_sensor.getAccel())        
        #print(imu_sensor.getAngularVelocity())