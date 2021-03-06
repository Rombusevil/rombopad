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
import threading, time, os, queue
from core.Pad import Pad
from common.Player import Player
from core.Recorder import Recorder
from metronome.Metronome import Metronome
from utils.AudioCropper import AudioCropper
from core.states.RecordState import RecordState
from core.states.PlaybackState import PlaybackState


class Main(object):
    def __init__(self):
        # Audio config
        self.chunk = 1024
        self.frameRate = 44100
        self.bitDepth = 16
        self.numChannels = 2

        # Init audio IO
        self.Recorder = Recorder(self.bitDepth, self.numChannels, self.frameRate, self.chunk)
        self.Player = Player(self.chunk)

        # Init pads
        self.cantPads = 8
        self.pads = []
        for pad in range(0,self.cantPads+1):
            self.pads.append(Pad(pad))

        # Init metronome
        self.Metronome = Metronome(self.chunk, self.frameRate, self.bitDepth, self.numChannels)

        # States
        self.rState = RecordState(self)
        self.pState = PlaybackState(self)
        self.State = self.pState    # It's on playing state by default

        # Queue player
        self.queue = queue.Queue()
        self.stopEvent = threading.Event()

        def queuePlayer(self, stopEvent):
            while not stopEvent.is_set():
                if(not self.queue.empty()):
                    self.Player.playFile(self.queue.get())
                else:
                    time.sleep(1)   # Queue is empty, sleep to reduce cpu usage
        self.playerThread = threading.Thread(target=queuePlayer, args=(self, self.stopEvent))
        self.playerThread.start()


    """ Stops queuePlayer thread
    """
    def clearThreads(self):
        self.stopEvent.set()


    """ Fill the queue with Pad's sound path
    """
    def play(self, padNumber):
        self.queue.put(Pad.getPathFromNumber(Pad, padNumber))

    """ Empty player queue
    """
    def stop(self):
        # TODO This doesn't stop playback, it just cleans playing queue
        with self.queue.mutex:
            self.queue.queue.clear()

    """ Plays 8 beats and then starts recording.
        Finally it crops output file in order to make it the exact length wanted
    """
    def record(self, padNumber, bpm, barBeats, countBars, beatsToRecord):
        # Creates a temp file for recording
        tmpPad =  self.pads[padNumber].getTmpAudioPath()

        # Creates metronome wave file
        mFile = self.Metronome.writeMetronome(bpm,(countBars*barBeats)+beatsToRecord)

        # Creo el thread de playback para grabar en este pad
        self.metronomeThread = threading.Thread(target=self.Metronome.playMetronome,args=(mFile, ))

        # Start recording
        self.Recorder.startRecording(tmpPad)
        self.metronomeThread.start()
        self.metronomeThread.join()             # Now waits until metronome playback finishes

        inLatency = self.Recorder.getLatency()
        outLatency = self.Metronome.getLatency()

        # Waits a spare time to compensate latency
        time.sleep(inLatency + outLatency)
        self.Recorder.stopRecording()

        # Now crop the temp file into the final file
        outFile = self.pads[padNumber].getAudioPath()

        # Create new AudioCropper every time in case bpm settings have changed.
        # With this the file is cropped to the exact length needed
        cropper = AudioCropper(bpm, barBeats, countBars, inLatency, outLatency)
        cropper.getValidRecording(tmpPad, outFile, beatsToRecord)

        # Delete temp file
        os.remove(tmpPad)

