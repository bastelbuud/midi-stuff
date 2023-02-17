# small demo programm, playing some music ( bach) on a pico over a midi out connection
# https://diyelectromusic.wordpress.com/2021/01/23/midi-micropython-and-the-raspberry-pi-pico/
# A 33Ω resistor is required to link to the 3.3V power and DIN pin 4;
# and a 10Ω resistor is required to link to the TX pin and DIN pin 5.
import machine
import time
import ustruct

pin = machine.Pin("LED", machine.Pin.OUT)
uart = machine.UART(1,31250)
#uart = machine.UART(1,9600)


notes = [69, 72, 74, 76, 72, 81, 79]
vels = [127, 96, 64, 96, 32, 127, 64]  # velocity per note
rests = [50, 50, 50, 50, 50, 200, 50]  # rests between notes
note_mods = [0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 5, 5, 3, 3]  # modifies notes for progression

while True:
    for j in range(0,16):  # loop through four measures progressions
        for i in range(0,7):
            pin.value(1)
            uart.write(ustruct.pack("bbb",0x90,notes[i]+note_mods[j], vels[i]))
            time.sleep(0.5)
            pin.value(0)
            time.sleep(0.5)
            uart.write(ustruct.pack("bbb",0x80,notes[i]+note_mods[j],0))
            #time.sleep(1)
            
            time.sleep(rests[i]/1000);


                              
