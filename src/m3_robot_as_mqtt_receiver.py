"""
Using a Brickman (robot) as the receiver of messages.
"""

# Same as m2_fake_robot_as_mqtt_sender,
# but have the robot really do the action.
# Implement just FORWARD at speeds X and Y is enough.


import mqtt_remote_method_calls as com
import time
import ev3dev.ev3 as ev3
import math


class DelegateThatReceives(object):

    def say_it(self, message):
        print("Message received!", message)

    def forward(self, arg1, arg2):

        print('New message', arg1, arg2)



def main():
    simple = SimpleRoseBot()
    name1 = input("Enter one name (subscriber): ")
    name2 = input("Enter another name (publisher): ")

    my_delegate = DelegateThatReceives()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect(name1, name2)
    time.sleep(1)  # Time to allow the MQTT setup.
    print()

    while True:
        time.sleep(0.01)  # Time to allow message processing

def wait_for_seconds(t):
    print ('Hello')
    start = time.time()
    while True:
        current = time.time()
        if current - start >= t:
            break
    print ('Goodbye')

class SimpleRoseBot(object):

    def __init__(self):
        self.lmotor = Motor('B')
        self.rmotor = Motor('C')

    def go(self,speed1,speed2):
        self.lmotor.turn_on(speed1)
        self.rmotor.turn_on(speed2)

    def go_distance(self,inches):
        self.lmotor.turn_on(100)
        self.rmotor.turn_on(100)
        start = self.rmotor.get_position() * (3.14*1.3)/360
        while True:
            end = self.rmotor.get_position() * (3.14*1.3)/360
            if end - start >= inches:
                break
        self.lmotor.turn_off()
        self.rmotor.turn_off()

class Motor(object):
    WheelCircumference = 1.3 * math.pi

    def __init__(self, port):  # port must be 'B' or 'C' for left/right wheels
        self._motor = ev3.LargeMotor('out' + port)

    def turn_on(self, speed):  # speed must be -100 to 100
        self._motor.run_direct(duty_cycle_sp=speed)

    def turn_off(self):
        self._motor.stop(stop_action="brake")

    def get_position(self):  # Units are degrees (that the motor has rotated).
        return self._motor.position

    def reset_position(self):
        self._motor.position = 0

main()
