# rombopad
Gnome App for recording loops with an octapad like interface for sequencing.


![alt tag](https://github.com/Rombusevil/rombopad/blob/master/docs/rombopad.png)


Rombopad is intended as a tool for arranging a musical composition.

It has a precise built in metronome and it records a predefined amount of beats,
this results in a looping audio file without the need of manually cropping.


Launching the app (inside src directory):
  **python3.4 run.py**

How to use:
  * Define BPM in the bottom left spinner.
  * Define the amount of beats to record in the bottom right spinner. Let's say, 8 beats for example.
  * Select Recording mode in the header bar.
  * Click on any pad, you'll hear the metronome sounding.
  * Prepare for recording after 8 metronome beats.
  * When the amount of beats to record reaches its end, the recording will stop automatically.
  * Select Playback mode in the header bar.
  * Click the same pad you've clicked to record, you'll hear the recorded sound.
  * If you click multiple pads, the sounds will queue up.
  

Dependencies:
  * Python3.4
  * PyAudio
  * Gtk+3


Notice:
  * It's in beta stage.
  * If you start a recording, you can't stop it. It will stop by itself when there are no more beats to record.
  * Avoid using "long" recording settings. When cropping, the audio file is held entirely in memory.
  * Pads are sequenced, once a pad started playing it won't stop until it finishes.
  * Class diagram is outdated.
