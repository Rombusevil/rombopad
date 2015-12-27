# -*- coding: utf-8 -*-
__author__ = 'Iber Parodi Siri'

"""
    This file is part of Rombopad.
    
    Rombopad is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Rombopad is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with Rombopad.  If not, see <http://www.gnu.org/licenses/>.
"""

import pyaudio, wave
from common.LatencyObject import LatencyObject

class Recorder(LatencyObject):
    def __init__(self, bitDepth=16, channels=1, rate=44100, framesPerBuffer=1024):
        self.channels = channels
        self.rate = rate
        self.fpb = framesPerBuffer
        self._stream = None
        self.latency = None
        self.bits_per_byte = 8
        self.bitDepth = bitDepth

    def startRecording(self, fileName):
        self._pa = pyaudio.PyAudio()
        self.wavefile = wave.open(fileName, 'wb')
        self.wavefile.setnchannels(self.channels)
        self.wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        self.wavefile.setframerate(self.rate)
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.fpb,
                                        stream_callback=self.getCallback())

        # Store stream latency
        self.latency = self._stream.get_input_latency()

        print ("Started recording.")
        self._stream.start_stream()
        return self

    def stopRecording(self):
        print ("Stopped recording.")
        self._stream.stop_stream()
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()
        return self

    def getCallback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback
