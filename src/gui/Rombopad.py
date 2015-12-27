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


from gi.repository import Gtk
from core.Main import Main

class Handler:
    def __init__(self, backend, builder):
        self.Backend = backend
        self.builder = builder

        self.BPM = None # Beats per minute
        self.BTR = None # Beats to record

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    """ Toggles de rec/play
    """
    def recBtnToggled(self, btn):
        self.Backend.State = self.Backend.rState if Gtk.ToggleButton.get_active(btn) else self.Backend.pState

        # Toggles the state of the other button
        playBtn = builder.get_object("statePlayBtn")
        Gtk.ToggleButton.set_active(playBtn, not Gtk.ToggleButton.get_active(btn) )

    def playBtnToggled(self, btn):
        self.Backend.State = self.Backend.pState if Gtk.ToggleButton.get_active(btn) else self.Backend.rState

        # Toggles the state of the other button
        recBtn = builder.get_object("stateRecBtn")
        Gtk.ToggleButton.set_active(recBtn, not Gtk.ToggleButton.get_active(btn) )

    """
       Pads
    """
    def padClicked(self, padNumber):
        barBeats = 4
        countBars = 2

        try:
            self.Backend.State.clicked(padNumber, int(self.BPM), barBeats, countBars, int(self.BTR))
        except None:
            print("No se cuantos beats grabar!!!")



    def p1Click(self, btn):
        self.padClicked(1)
    def p2Click(self, btn):
        self.padClicked(2)
    def p3Click(self, btn):
        self.padClicked(3)
    def p4Click(self, btn):
        self.padClicked(4)
    def p5Click(self, btn):
        self.padClicked(5)
    def p6Click(self, btn):
        self.padClicked(6)
    def p7Click(self, btn):
        self.padClicked(7)
    def p8Click(self, btn):
        self.padClicked(8)

    """
        Spinners
    """
    def bpmSpinner(self, spinButton):
        self.BPM = spinButton.get_value()
        print(" Setted BPM: "+ str(spinButton.get_value()))

    def btrSpinner(self, spinButton):
        self.BTR = spinButton.get_value()
        print(" Setted BTR: "+str(spinButton.get_value()))






# El main está apartir de esta línea
builder = Gtk.Builder()
builder.add_from_file("gui.xml")


handler = Handler( Main(), builder)
builder.connect_signals( handler )

# Widgets UI
window = builder.get_object("mainWindow")
bpmSpinner = builder.get_object("tempoSp")
btRecord = builder.get_object("recordBeatsSp")

# Spinners
bpmAdj = Gtk.Adjustment(value=120, lower=30, upper=300, step_incr=1, page_incr=10, page_size=10)
btRecordAdj = Gtk.Adjustment(value=4, lower=1, upper=100, step_incr=1, page_incr=10, page_size=10)

bpmSpinner.set_adjustment(bpmAdj)
btRecord.set_adjustment(btRecordAdj)



print(type(bpmSpinner))

window.show_all()

Gtk.main()
