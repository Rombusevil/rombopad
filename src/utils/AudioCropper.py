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




    This class crops the recorder audio to fit the precise timing of the
    recorder bars wanted.
"""

import wave

class AudioCropper(object):
    def __init__(self, bpm, barBeats, countBars, inLatency, outLatency):
        self.bpm = bpm
        self.bps = bpm/60
        self.beatsPerBar = barBeats
        self.inLat = inLatency      # Input stream latency at the time of recording this sound
        self.outLat = outLatency    # Output stream latency at the time of playing the metronome while recording
        self.countBars = countBars  # Amount of bars counted before recording

    """
        Devuelve el segmento del audio grabado que contiene
        la grabación válida. Es decir, la cantidad de bars
        predefinidas para la grabación.
    """
    def getValidRecording(self, inFile, outFile, recordedBeats):
        wIn = wave.open(inFile, 'rb')
        wOut= wave.open(outFile, 'wb')

        latency = (self.inLat + self.outLat) * 0.10     # Change the unit

        # Seconds to remove at the begining (I'm recording initial "count" beats, so now I have to remove them)
        inSecsRem      = (self.countBars * self.beatsPerBar)/ self.bps

        # Seconds of valid recording to retain
        secsToRecord   =  recordedBeats / self.bps

        marker1 = latency+inSecsRem     # En segundos, el momento donde comienza la grabación válida. Relativo al archivo
        marker2 = marker1+secsToRecord  # En segundos, el momento donde termina la grabación válida. Relativo al archivo

        # Convert markers to frames
        frameMarker1, frameMarker2 = int(marker1*wIn.getframerate()), int(marker2*wIn.getframerate())

        # Dispose every frame before marker 1
        wIn.readframes(frameMarker1)

        # Keep every frame between marker 1 and marker 2
        frames = wIn.readframes(frameMarker2-frameMarker1)

        # Spit out the cropped file
        wOut.setparams(wIn.getparams())
        wOut.writeframes(frames)

        wIn.close()
        wOut.close()