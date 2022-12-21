/*
  MIDI Bach notes player

  This sketch shows how to use the serial transmit pin (pin 1) to send MIDI note data.
  If this circuit is connected to a MIDI device ( we use garageband on the Mac) it plays some notes of Bach Music

  The circuit:
  - digital in 1 connected to MIDI jack pin 5
  - MIDI jack pin 2 connected to ground
  - MIDI jack pin 4 connected to +5V through 220 ohm resistor
  - Attach a MIDI cable to the jack, then to a MIDI synth, and play music.

  created 13 Jun 2006
  modified 13 Aug 2012
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Midi
*/

const int mynotes [] = {0x60,0x61,0x62,0x63,0x64,0x63,0x62,0x61};
void setup() {
  // Set MIDI baud rate:
  Serial.begin(31250);
}

void loop() {
  // play the array of notes we defined in mynotes
  for (int note : mynotes) {
    //Note on channel 1 (0x90), some note value (note), middle velocity (0x45):
    noteOn(0x90, note, 127);
    delay(100);
    //Note on channel 1 (0x90), some note value (note), silent velocity (0x00):
    noteOn(0x80, note, 0x00);
    delay(100);
  }
}

// plays a MIDI note. 
void noteOn(int cmd, int pitch, int velocity) {
  Serial.write(cmd);
  Serial.write(pitch);
  Serial.write(velocity);
}
