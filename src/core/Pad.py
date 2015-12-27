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

class Pad(object):
    def __init__(self, padNumber): #, Player, Recorder):
#        self.Player = Player
#        self.Recorder = Recorder
        self.audioPath = "/home/rombus/.rombopad/pad"+str(padNumber)+".wav"


    """ Tells the player object to play this pad's audio
    """
#    def play(self):
#        self.Player.playFile(self.audioPath)

    """ Tells the recorder object to record this pad's audio
    """
#    def record(self, duration):
#        self.Recorder.recordFile(duration)

    """ Returns the wave file path associated with this pad
    """
    def getAudioPath(self):
        return self.audioPath