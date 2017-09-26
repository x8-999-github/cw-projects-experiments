# Authors: y8
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
import logging
import time
from chipwhisperer.common.utils import util

from base import ScopeTemplate,Channel
from chipwhisperer.common.utils.pluginmanager import Plugin
from chipwhisperer.common.utils.parameter import Parameter, setupSetParam
import numpy

#
#https://github.com/python-ivi/python-vxi11
#
#diff --git a/vxi11/rpc.py b/vxi11/rpc.py
#index 9d889a6..c744f8c 100644
#--- a/vxi11/rpc.py
#+++ b/vxi11/rpc.py
#@@ -257,6 +257,7 @@ class RawTCPClient(Client):
# 
#     def connect(self):
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#+       self.sock.settimeout(2.0)
#         self.sock.connect((self.host, self.port))
# 
#     def close(self):

import vxi11

class DS1000z(ScopeTemplate,Plugin):
    _name = "Rigol DS1000Z Series scopes"

    def __init__(self):        
        ScopeTemplate.__init__(self)
        self.dataUpdated = util.Signal()
        self.dataUpdated.connect(self.newDataReceived)
        self.visa_str ="TCPIP::10.16.82.186::INSTR"
        self.channels = [Channel(self.getName() + " - Channel " + str(n)) for n in range(1)]

        self.params.addChildren([
            {'name':'VISA resource string', 'type':'str', 'get':self.visaStr, 'set':self.setVisaStr}
        ])        
        self.params.init()
        self.intr = None
        
        
        
    @setupSetParam("VISA resource string")
    def setVisaStr(self,visa_str):
        self.visa_str = visa_str

    def visaStr(self):
        return self.visa_str

    def _con(self):        
        self.instr = vxi11.Instrument(self.visa_str)
        try:
            self.instr.open()
        except Exception as e:
            logging.warning("Can not open connection to scope %s:%s" % (self.visa_str,str(e)))
            return False
        return True

    def _dis(self):
        if self.instr:
            self.instr.close()
    
    def arm(self):
        if self.connectStatus.value() is False:
            raise Exception("Scope \"" + self.getName() + "\" is not connected. Connect it first...")

        #Configure for single shot
        self.instr.write(":SINGLE")

        #Wait for the scope to be in WAIT state        
        stat = self.instr.ask(":TRIG:STAT?")

        counter = 10
        while stat != "WAIT":                    
            if counter == 0:
                break
            else:
                time.sleep(0.1)
                counter = counter -1

            stat = self.instr.ask(":TRIG:STAT?")

        if stat != "WAIT":
            logging.warning("Expected scope trigger status to be WAIT but it was %s" % stat)

    def capture(self,timeout_s=5):
        timeout_s = 5 

        stat = self.instr.ask(":TRIG:STAT?")
        time_end = time.time() + timeout_s

        while time_end > time.time():
            self.instr.ask(":TRIG:STAT?")            
            if stat == "STOP":
                break
            time.sleep(0.2)
            util.updateUI()

        if stat != "STOP":
            logging.warning("Timeout while capturing")
            return False

        self.instr.write(":WAV:SOUR CHAN3")
        self.instr.write(":WAV:FORM BYTE")
        self.instr.write(":WAV:DATA?")
        
        rawdata = self.instr.read_raw()
        if rawdata[0] != '#':
            raise IOError('Error in header')
        
        #
        # The header format is the following
        # MARKER|HEADER_SIZE_COUNT|DATA_SIZE      |DATA
        # byte #| byte c          |BCD of c bytes |DATA
        hdrlen = rawdata[1]
        hdrlen = int(hdrlen)
        datalen = rawdata[2:(2+hdrlen)]
        datalen = int(datalen)
        data = numpy.frombuffer(rawdata, dtype='B', offset=hdrlen + 2, count=datalen)
        self.dataUpdated.emit(0, data)


if __name__ == '__main__':
    print("DS1000z test code")
    ds =  DS1000z()
    ds.con()
    ds.arm()
    ds.capture()

    
