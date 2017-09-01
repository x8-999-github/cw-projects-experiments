from chipwhisperer.hardware.naeusb.naeusb import NAEUSB
from chipwhisperer.hardware.naeusb.fpga import FPGA
import binascii

cwtestusb = NAEUSB()
cwtestusb.con()
fpga = FPGA(cwtestusb)

if fpga.isFPGAProgrammed() == False:
    print("Programming the FPGA")
    fpga.FPGAProgram(open("cwlite_interface.bit"))

# read software registers

# test echo
#cwtestusb.cmdWriteMem(0x04,"K")

#print( cwtestusb.cmdReadMem(0x04,1))

def b2hex(in_b):
    return ''.join('{:02x}'.format(x) for x in in_b)

version = cwtestusb.cmdReadMem(0x07,4)

print( b2hex(version))