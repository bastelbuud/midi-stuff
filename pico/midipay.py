# small demo programm, playing some music ( bach) on a pico over a midi out connection
# https://diyelectromusic.wordpress.com/2021/01/23/midi-micropython-and-the-raspberry-pi-pico/
# A 33Ω resistor is required to link to the 3.3V power and DIN pin 4;
# and a 10Ω resistor is required to link to the TX pin and DIN pin 5.
import machine
import time
import ustruct

pin = machine.Pin("LED", machine.Pin.OUT)
uart = machine.UART(1,31250)

notes = [60,61,62,63,64,63,62,61]

while True:
  for x in notes:
    pin.value(1)
    uart.write(ustruct.pack("bbb",0x90,x,127))
    time.sleep(0.5)
    pin.value(0)
    time.sleep(0.5)
    uart.write(ustruct.pack("bbb",0x80,x,0))