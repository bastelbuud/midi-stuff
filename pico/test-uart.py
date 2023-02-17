import machine

uart = machine.UART(0,31250)
pin = machine.Pin("LED", machine.Pin.OUT)

while True:
    if (uart.any()):
        print("0x{0:02x}".format(uart.read(1)[0]))
        pin.value(1)
    else :
        pin.value(0)