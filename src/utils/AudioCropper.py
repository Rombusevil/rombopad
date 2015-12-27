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

import wave

class AudioCropper(object):

    """
        Configuraciones globales para el Audio Cropper

        bpm : int
            Beats per minute
        barBeats : int
            Beats per bar
        countBeats : int
            Number of beats before recording starts
        inLatency : float
            Input latency of the recorder stream
        outLatency : float
            Output latency of the playback stream
    """
    def __init__(self, bpm, barBeats, countBars, inLatency, outLatency):
        self.bpm = bpm
        self.bps = bpm/60
        self.beatsPerBar = barBeats
        self.inLat = inLatency
        self.outLat = outLatency
        self.countBars = countBars

    """
        Devuelve el segmento del audio grabado que contiene
        la grabación válida. Es decir, la cantidad de bars
        predefinidas para la grabación.
    """
    def getValidRecording(self, inFile, outFile, recordedBeats):
        wIn = wave.open(inFile, 'rb')
        wOut= wave.open(outFile, 'wb')

        latency = (self.inLat + self.outLat) * 0.10 # Lo multiplico por 0.10 para cambiarlo de unidad

        # Segundos a eliminar del principio (los clicks de metrónomo que cuenta antes de empezar a grabar)
        inSecsRem      = (self.countBars * self.beatsPerBar)/ self.bps
        # Segundos de grabación válida a mantener
        #secsToRecord   = (recordedBars * self.beatsPerBar)  / self.bps
        secsToRecord   =  recordedBeats / self.bps

        marker1 = latency+inSecsRem         # En segundos, el momento donde comienza la grabación válida. Relativo al archivo
        marker2 = marker1+secsToRecord  # En segundos, el momento donde termina la grabación válida. Relativo al archivo

        # Convierto los markers en frames
        frameMarker1, frameMarker2 = int(marker1*wIn.getframerate()), int(marker2*wIn.getframerate())

        # Descarto todos los frames anteriores al tiempo del marker1
        wIn.readframes(frameMarker1)

        # Leo todos los frames comprendidos entre marker1 y marker2
        frames = wIn.readframes(frameMarker2-frameMarker1)

        # Genero el archivo croppeado
        wOut.setparams(wIn.getparams())
        wOut.writeframes(frames)

        wIn.close()
        wOut.close()