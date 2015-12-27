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





    This class is able of generating wave files with metronome data.
    It depends on common/Player.py for playing the metronome wav file.
"""
from common.Player import Player
import wave

class Metronome(object):
    def __init__(self, chunk=1024, frameRate=44100, bitDepth=16, numChannels=2):
        self.Player = Player(chunk)         # Own Player object for playing back the metronome file
        self.chunk = chunk
        self.frame_rate = frameRate
        self.bit_depth = bitDepth
        self.num_channels = numChannels
        self.bits_per_byte = 8
        self.silence = b'\x00'              # This is how one frame of silence is represented in wave files


    """ Writes wave file with metronome data
    """
    def writeMetronome(self, bpm, cantBeats):
        duration = self._getFramesDuration(bpm, cantBeats) # Duration of the output audio file (in frames)

        # Creates the output file with it's wave header
        outPath = "metronome"+str(bpm)+".wav"
        wOut = wave.open(outPath,"w")
        wOut.setparams((self.num_channels, (self.bit_depth // self.bits_per_byte), self.frame_rate, duration, 'NONE', 'not compressed'))

        # Reads beat sound in memory
        beatPath= '../metronome/beat.wav'
        beatData = self._getBeatData(beatPath)
        beatSound = b''.join(b for b in beatData)

        # Spacing of beats (in frames)
        spacing = self._getBeatSpacing(bpm)


        # Start sequence of generating a metronome inside a wave file
        wOut.writeframes(beatSound)         # Writes the first beat to the file (later we need to write the adjacent silence)
        curPos = wOut.tell()                # Te amount of frames of one beat
        silencedFrames = spacing - curPos   # This calculates the amount of silence (in frames) needed

        # Generates audio silence data
        if (silencedFrames > 0):
            silenceData = self.silence * int(silencedFrames)
            silenceData *= 4                            # Convert Quarter not to Whole note
            wOut.writeframes(bytearray(silenceData))    # Writes silence frames corresponding to the first beat written
        else:
            print("Invalid BPM!!!")
            return

        # Finish writing remaining beats
        while True:
            wOut.writeframes(beatSound)
            wOut.writeframes(bytearray(silenceData))

            if(wOut.tell() >= duration): # If current position excceds duration where're done
                break

        wOut.close()
        return outPath


    """ Play metronome
    """
    def playMetronome(self, metronomeFile):
        self.Player.playFile(metronomeFile)


    """ Returns the beat sound data from a specific metronome audio click file
    """
    def _getBeatData(self, beatPath):
        beatSound = wave.open(beatPath,'r')
        beatSound.readframes(44)    # Ignores wave header

        # Fills dataArr with the sound of beatPath
        dataArr = []
        while True:
            sample = beatSound.readframes(self.chunk)

            if(sample.__sizeof__() < self.chunk):
                break

            dataArr.append(sample)

        return dataArr


    """ Returns spacing of beats (in frames) according to BPM
    """
    def _getBeatSpacing(self, bpm):
        bps = bpm / 60                      # Beats per second
        spacing = self.frame_rate // bps    # Spacing in between beats (in frames)

        return spacing

    """ Returns duration of output metronome wav file (in frames)
    """
    def _getFramesDuration(self, bpm, cantBeats):
        spacing = self._getBeatSpacing(bpm)
        return int(spacing * cantBeats)


    """ Returns output stream latency
    """
    def getLatency(self):
        return self.Player.getLatency()