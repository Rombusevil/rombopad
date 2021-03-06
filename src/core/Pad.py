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
from os.path import expanduser

class Pad(object):
    def __init__(self, padNumber): #, Player, Recorder):
        path = self._getPath(self)
        self.audioPath   = path+ "pad"  +str(padNumber)+".wav"
        self.tmpAudioPath= path+ ".pad" +str(padNumber)+".wav"

    """ Returns the wave file path associated with this pad
    """
    def getAudioPath(self):
        return self.audioPath

    """ Returns the wave file path associated with this pad tmp file
    """
    def getTmpAudioPath(self):
        return self.tmpAudioPath


    """ Static method for converting padNumber into it's corresponding audio path
    """
    @staticmethod
    def getPathFromNumber(self, padNumber):
        path = self._getPath(self)
        return path+ "pad"  +str(padNumber)+".wav"


    """ My take on static variables
        If you want to change the base path, do it here.
    """
    @staticmethod
    def _getPath(self):
        return expanduser("~") + "/.rombopad/"