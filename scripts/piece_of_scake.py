#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014, NewAE Technology Inc
# All rights reserved.
#
# Authors: Colin O'Flynn
#
# Find this and more at newae.com - this file is part of the chipwhisperer
# project, http://www.assembla.com/spaces/chipwhisperer
#
#    This file is part of chipwhisperer.
#
#    chipwhisperer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    chipwhisperer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with chipwhisperer.  If not, see <http://www.gnu.org/licenses/>.
#=================================================

from chipwhisperer.common.api.CWCoreAPI import CWCoreAPI  # Import the ChipWhisperer API
from chipwhisperer.common.scripts.base import UserScriptBase


class UserScript(UserScriptBase):
    _name = "Solution for RHME2 piece of scake using an external serial"
    _description = "Solution for RHME2 piece of scake using an external serial"

    def __init__(self, api):
        super(UserScript, self).__init__(api)

    def run(self):
        # User commands here
        self.api.setParameter(['Generic Settings', 'Scope Module', 'ChipWhisperer/OpenADC'])        
        self.api.setParameter(['Generic Settings', 'Target Module', 'Simple Serial'])
        self.api.setParameter(['Generic Settings', 'Trace Format', 'ChipWhisperer/Native'])
        self.api.setParameter(['ChipWhisperer/OpenADC', 'Connection', 'NewAE USB (CWLite/CW1200)'])
                
      

        self.api.setParameter(['Simple Serial', 'Connection', 'System Serial Port'])
        self.api.setParameter(['Simple Serial', 'System Serial Port', 'Baud', '19200'])        
        self.api.setParameter(['Simple Serial', 'System Serial Port', 'Port', '/dev/ttyUSB0'])
        self.api.setParameter(['Simple Serial', 'Protocol Version', 'Version', '1.0'])
        self.api.setParameter(['Simple Serial', 'Protocol format', 'bin'])
        self.api.connect()
       # 
        self.api.setParameter(['Simple Serial', 'Load Key Command', u''])
        self.api.setParameter(['Simple Serial', 'Go Command', "65$TEXT$0A"])
        self.api.setParameter(['Simple Serial', 'Output Format', u'$RESPONSE$'])
        # Example of using a list to set parameters. Slightly easier to copy/paste in this format
        lstexample = [['CW Extra Settings', 'Trigger Pins', 'Target IO4 (Trigger Line)', True],
                      ['CW Extra Settings', 'Target IOn Pins', 'Target IO1', 'Serial RXD'],
                      ['CW Extra Settings', 'Target IOn Pins', 'Target IO2', 'Serial TXD'],
                      ['OpenADC', 'Clock Setup', 'CLKGEN Settings', 'Desired Frequency', 16000000.0],
                      ['CW Extra Settings', 'Target HS IO-Out', 'CLKGEN'],
                      ['OpenADC', 'Clock Setup', 'ADC Clock', 'Source', 'CLKGEN x4 via DCM'],
                      ['OpenADC', 'Trigger Setup', 'Total Samples', 6000],
                      ['OpenADC', 'Trigger Setup', 'Offset', 3000],
                      ['OpenADC', 'Gain Setting', 'Setting', 45],
                      ['OpenADC', 'Trigger Setup', 'Mode', 'rising edge'],
                      # Final step: make DCMs relock in case they are lost
                      ['OpenADC', 'Clock Setup', 'ADC Clock', 'Reset ADC DCM', None],
                      ]
        
        # Download all hardware setup parameters
        for cmd in lstexample: self.api.setParameter(cmd)
        
        # Let's only do a few traces
        self.api.setParameter(['Generic Settings', 'Acquisition Settings', 'Number of Traces', 50])
                      
        # Throw away first few
        #self.api.capture1()

        # Capture a set of traces and save the project
        # self.api.captureM()
        # self.api.saveProject("../../../projects/test.cwp")


if __name__ == '__main__':
    import chipwhisperer.capture.ui.CWCaptureGUI as cwc         # Import the ChipWhispererCapture GUI
    from chipwhisperer.common.utils.parameter import Parameter  # Comment this line if you don't want to use the GUI
    Parameter.usePyQtGraph = True                               # Comment this line if you don't want to use the GUI
    api = CWCoreAPI()                                           # Instantiate the API
    app = cwc.makeApplication("Capture")                        # Change the name if you want a different settings scope
    gui = cwc.CWCaptureGUI(api)                                 # Comment this line if you don't want to use the GUI
    api.runScriptClass(UserScript)                              # Run the User Script (executes "run()" by default)
    app.exec_()                                                 # Comment this line if you don't want to use the GUI
