import Gamepad
import time
import RPi.GPIO as gpio
import sys

gpio.setmode(gpio.BOARD)

gpio.setup(12, gpio.OUT)
gpio.setup(32, gpio.OUT)
gpio.setup(33, gpio.OUT)
gpio.setup(35, gpio.OUT)

pwm_1 = gpio.PWM(12, 1000)
pwm_2 = gpio.PWM(32, 1000)
pwm_3 = gpio.PWM(33, 1000)
pwm_4 = gpio.PWM(35, 1000)

max_duty_cycle = 65
slow_mode_duty_cycle = 50

slow_mode = false

gamepadType = Gamepad.XboxONE

if not Gamepad.available():
	print("Please connect you gamepad...")
	while not Gamepad.available():
		time.sleep(1)
gamepad = gamepadType()
print("Controller Connected")

gamepad.startBackgroundUpdates()

try:
	pwm_1.start(0)
	pwm_2.start(0)
	pwm_3.start(0)
	pwm_4.start(0)
	while gamepad.isConnected():
		if gamepad.isPressed("B"):
			pwm_1.ChangeDutyCycle(max_duty_cycle)
			pwm_2.ChangeDutyCycle(0)
			pwm_3.ChangeDutyCycle(0)
			pwm_4.ChangeDutyCycle(max_duty_cycle)
		else:
			direction = gamepad.isPressed("A");
			if gamepad.beenPressed("X"):
				slow_mode = !slow_mode
			if gamepad.beenPressed("Y"):
				break
			#if gamepad.beenPressed("A"):
			#	print("A")
			right_speed = (gamepad.axis("RT") + 1.0) / 2.0
			left_speed = (gamepad.axis("LT") + 1.0) / 2.0

			right_final = max_duty_cycle * right_speed if not slow_mode else max_back_duty_cycle * right_speed
			left_final = max_duty_cycle * left_speed if not slow_mode else max_back_duty_cycle * left_speed

			if direction:
				pwm_1.ChangeDutyCycle(left_final)
				pwm_2.ChangeDutyCycle(0)
				pwm_3.ChangeDutyCycle(right_final)
				pwm_4.ChangeDutyCycle(0)
			else:
				pwm_1.ChangeDutyCycle(0)
				pwm_2.ChangeDutyCycle(left_final)
				pwm_3.ChangeDutyCycle(0)
				pwm_4.ChangeDutyCycle(right_final)
		
finally:
	gpio.cleanup()
	gamepad.disconnect()



