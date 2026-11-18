import serial
import time
from pynput import keyboard

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1.0)
time.sleep(3)              # ESP32 resets when the port opens
ser.reset_input_buffer()

print('Hold W/S = motor forward/backward | A/D = servo left/right | ESC = quit')

pressed = set()
running = True

def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        return False
    try:
        pressed.add(key.char.lower())
    except AttributeError:
        pass

def on_release(key):
    try:
        pressed.discard(key.char.lower())
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

try:
    while running:
        w, s = 'w' in pressed, 's' in pressed
        a, d = 'a' in pressed, 'd' in pressed

        if w and not s:
            motor = 'W'
        elif s and not w:
            motor = 'S'
        else:
            motor = 'X'

        if a and not d:
            servo = 'A'
        elif d and not a:
            servo = 'D'
        else:
            servo = 'N'

        ser.write((motor + servo + '\n').encode('utf-8'))
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    listener.stop()
    ser.write(b'XN\n')     # stop the motor
    ser.close()
    print('closed')