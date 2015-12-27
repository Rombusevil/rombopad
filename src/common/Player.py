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


""" This class knows how to play audio, it just needs a wave file path
"""
import pyaudio, wave
from common.LatencyObject import LatencyObject

class Player(LatencyObject):
    def __init__(self, chunk):
        self.chunk = chunk
        self.latency = None


    def playFile(self, fileToPlay):
        try:
            wIn = wave.open(fileToPlay,"rb")
        except:
            # File doesn't exists!!!
            print("Can't play "+fileToPlay+"!!!")
            return

        paudio = pyaudio.PyAudio()
        stream = paudio.open(format = paudio.get_format_from_width(wIn.getsampwidth()),
                        channels = wIn.getnchannels(),
                        rate = wIn.getframerate(),
                        output = True)

        # Store stream latency
        self.latency = stream.get_output_latency()

        # Play sound
        while True:
            data = wIn.readframes(self.chunk)
            stream.write(data)

            # Exit if EOF reached
            if(data.__sizeof__() < self.chunk):
                break

        stream.stop_stream()
        stream.close()
        paudio.terminate()