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

import os
import shutil

import chipwhisperer.capture.ui.CWCaptureGUI as cwc       # Import the ChipWhispererCapture GUI
from chipwhisperer.capture.api.programmers import XMEGAProgrammer
from chipwhisperer.common.api.CWCoreAPI import CWCoreAPI  # Import the ChipWhisperer API4
from chipwhisperer.common.scripts.base import UserScriptBase
from chipwhisperer.common.utils.parameter import Parameter
import chipwhisperer.tests

# Wiki: https://wiki.newae.com/Tutorial_A2_Introduction_to_Glitch_Attacks_(including_Glitch_Explorer)
# Adding an additional parameter for the glitching (offset)

class UserScript(UserScriptBase):
    _name = "Test the Glitch offset and width"

    def __init__(self, api):
        super(UserScript, self).__init__(api)
        self.pname = "glitchtest_offset_and_width"

    def run(self):
        # Delete previous project files
        if os.path.isfile("projects/%s.cwp" % self.pname): os.remove("projects/%s.cwp" % self.pname)
        #shutil.rmtree("projects/%s_data" % self.pname, ignore_errors=True)

        # Save current open project (default) to a new place
        self.api.saveProject("projects/%s.cwp" % self.pname)

        print "Software Setup - 1. Connect to the ChipWhisperer device:"
        self.api.setParameter(['Generic Settings', 'Scope Module', 'ChipWhisperer/OpenADC'])
        self.api.setParameter(['Generic Settings', 'Target Module', 'Simple Serial'])
        self.api.setParameter(['Generic Settings', 'Trace Format', 'None'])
        self.api.setParameter(['Simple Serial', 'Connection', 'NewAE USB (CWLite/CW1200)'])
        self.api.setParameter(['ChipWhisperer/OpenADC', 'Connection', 'NewAE USB (CWLite/CW1200)'])
        # Connect to both: scope and target
        self.api.connect()

        print "Software Setup - 2. Setup the CLKGEN Module to Generate a 7.37 MHz clock and route it through the Glitch Generator"
        lstexample = [
            ['OpenADC', 'Clock Setup', 'Freq Counter Src', 'CLKGEN Output'],
            ['OpenADC', 'Clock Setup', 'CLKGEN Settings', 'Desired Frequency', 7370000.0],
            ['OpenADC', 'Clock Setup', 'ADC Clock', 'Reset ADC DCM', None],
            ['Glitch Module', 'Clock Source', 'CLKGEN'],
            ['CW Extra Settings', 'Target HS IO-Out', 'Glitch Module'],
        ]
        for cmd in lstexample: self.api.setParameter(cmd)

        print "Software Setup - 3. Connect the Serial Port"
        lstexample = [
            ['CW Extra Settings', 'Target IOn Pins', 'Target IO1', 'Serial RXD'],
            ['CW Extra Settings', 'Target IOn Pins', 'Target IO2', 'Serial TXD']
        ]
        for cmd in lstexample: self.api.setParameter(cmd)



        print "Manual Glitch Trigger"
        lstexample = [
            ['Glitch Module', 'Glitch Width (as % of period)', 9.5],
            ['Glitch Module', 'Glitch Offset (as % of period)', -4],
            ['Glitch Module', 'Repeat', 1],
            ['Glitch Module', 'Glitch Trigger', 'Manual'],
            ['Glitch Module', 'Manual Trigger / Single-Shot Arm', None],  # Push the button
        ]
        for cmd in lstexample: self.api.setParameter(cmd)

        print "Automatically Resetting Target"
        lstexample = [
            ['Generic Settings', 'Auxiliary Module', 'Reset AVR/XMEGA via CW-Lite'],
            ['Aux Settings', 'Reset AVR/XMEGA via CW-Lite', 'Interface', 'xmega (PDI)'],
            ['Aux Settings', 'Reset AVR/XMEGA via CW-Lite', 'Test Reset', None],  # Push the button
            ['Simple Serial', 'Load Key Command', u''],
            ['Simple Serial', 'Go Command', u'test\n'], # Enter wrong password
            ['Simple Serial', 'Output Format', u''],
            ['Simple Serial', 'Protocol Version', 'Version', '1.0'], # Prevent sending 'v'
        ]
        for cmd in lstexample: self.api.setParameter(cmd)
        self.api.capture1()
        self.api.capture1()
        self.api.capture1()

        print "Automatically Triggering Glitch - Enable the power analysis capture"
        lstexample = [
            ['OpenADC', 'Clock Setup', 'ADC Clock', 'Source', 'CLKGEN x4 via DCM'],
            ['OpenADC', 'Clock Setup', 'ADC Clock', 'Reset ADC DCM', None],  # Push the button
            ['OpenADC', 'Trigger Setup', 'Mode', 'rising edge'],
            ['OpenADC', 'Trigger Setup', 'Total Samples', 1000],
            ['OpenADC', 'Gain Setting', 'Setting', 40],
        ]
        for cmd in lstexample: self.api.setParameter(cmd)
        self.api.capture1()
        self.api.capture1()
        self.api.capture1()

        print "Automatically Triggering Glitch - Enable the trigger of the glitch to occur based on this external trigger pin"
        self.api.setParameter(['Glitch Module', 'Glitch Trigger', 'Ext Trigger:Single-Shot'])
        self.api.capture1()
        self.api.capture1()
        self.api.capture1()

        print "Using the Glitch Explorer"
        self.api.setParameter(['Simple Serial', 'Output Format', u'$GLITCH$'])
        self.api.capture1()
        self.api.capture1()
        self.api.capture1()
        lstexample = [
            ['Glitch Explorer', 'Normal Response', u"s == 'Denied\\nPassword:'"],
            ['Glitch Explorer', 'Successful Response', u"'Welcome' in s"],
        ]
        for cmd in lstexample: self.api.setParameter(cmd)
        self.api.capture1()
        self.api.capture1()
        self.api.capture1()

        print "Using the Glitch Explorer -  Tune the glitch offset to attempt to get a successful clock glitch"
        self.api.setParameter(['Glitch Explorer', 'Plot Widget', None])  # Push the button
        lstexample = [
            ['Glitch Explorer', 'Tuning Parameters', 1],
            ['Glitch Explorer', 'Tuning Parameter 0', 'Name', u'Offset'],
            ['Glitch Explorer', 'Tuning Parameter 0', 'Parameter Path', u"['Glitch Module', 'Ext Trigger Offset']"],
            ['Glitch Explorer', 'Tuning Parameter 0', 'Data Format', 'Int'],
            ['Glitch Explorer', 'Tuning Parameter 0', 'Range', (0, 100)],
            ['Glitch Explorer', 'Tuning Parameter 0', 'Value', 0],
            ['Glitch Explorer', 'Tuning Parameter 0', 'Step', 1],
            ['Glitch Explorer', 'Tuning Parameter 0', 'Repeat', 1],
            ['Glitch Module', 'Repeat', 1],
            ['Glitch Explorer', 'Traces Required', 'Use this value', None], # Press "use this value"             
        ]
        for cmd in lstexample: self.api.setParameter(cmd)
        

if __name__ == '__main__':
    app = cwc.makeApplication()                     # Comment this line if you don't want to use the GUI
    Parameter.usePyQtGraph = True                   # Comment this line if you don't want to use the GUI
    api = CWCoreAPI()                               # Instantiate the API
    gui = cwc.CWCaptureGUI(api)                     # Comment this line if you don't want to use the GUI
    gui.glitchMonitor.show()
    gui.serialTerminal.show()
    api.runScriptClass(UserScript)                  # Run the User Script
    app.exec_()