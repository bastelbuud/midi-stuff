# Simple MIDI Monitor
# must run on uart 0, uart1 delivers wrong info !!!
import machine
import utime
import ustruct

pin = machine.Pin("LED", machine.Pin.OUT)
uart = machine.UART(0,31250)
#uart.init(31250, bits=8, parity=None, stop=1,invert=machine.UART.INV_RX)

# Basic MIDI handling commands
def doMidiNoteOn(note,vel):
    pin.value(1)
    print("Note On \t", note, "\t", vel)

def doMidiNoteOff(note,vel):
    pin.value(0)
    print("Note Off\t", note, "\t", vel)


MIDICH = 1
MIDIRunningStatus = 0
MIDINote = 0
MIDILevel = 0
def doMidi(mb):
    global MIDIRunningStatus
    global MIDINote
    global MIDILevel
    print("0x{0:02x}".format(mb))
    uart.write(ustruct.pack("b",mb))
    if ((mb >= 0x80) and (mb <= 0xEF)):
        # MIDI Voice Category Message.
        # Action: Start handling Running Status
        MIDIRunningStatus = mb
        MIDINote = 0
        MIDILevel = 0
    elif ((mb >= 0xF0) and (mb <= 0xF7)):
        # MIDI System Common Category Message.
        # Action: Reset Running Status.
        MIDIRunningStatus = 0
    elif ((mb >= 0xF8) and (mb <= 0xFF)):
        # System Real-Time Message.
        # Action: Ignore these.
        pass
    else:
        # MIDI Data
        if (MIDIRunningStatus == 0):
            # No record of what state we're in, so can go no further
            return
        if (MIDIRunningStatus == (0x80|(MIDICH-1))):
            # Note OFF Received
            if (MIDINote == 0):
                # Store the note number
                MIDINote = mb
            else:
                # Already have the note, so store the level
                MIDILevel = mb
                doMidiNoteOff (MIDINote, MIDILevel)
                MIDINote = 0
                MIDILevel = 0
        elif (MIDIRunningStatus == (0x90|(MIDICH-1))):
            # Note ON Received
            if (MIDINote == 0):
                # Store the note number
                MIDINote = mb
            else:
                # Already have the note, so store the level
                MIDILevel = mb
                if (MIDILevel == 0):
                    doMidiNoteOff (MIDINote, MIDILevel)
                else:
                    doMidiNoteOn (MIDINote, MIDILevel)
                MIDINote = 0
                MIDILevel = 0
        else:
            # This is a MIDI command we aren't handling right now
            pass

while True:
    if (uart.any()):
        pin.value(1)
        doMidi(uart.read(1)[0])
    else:
        pin.value(0)