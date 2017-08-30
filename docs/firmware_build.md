# ChipWhisperer building the firmware

The ChipWhispere FPGA firmware can be built from within the normal source tree.

## Prerequisites

The ChipWhisperer lite (CW from now on) contains an Xilinx series FPGA 6SLX9TQG144
FPGA. To be able to compile this code you need to download the xilinx websuite. This is older software still works nice for the 6 series FGPA's.

Setup the environemnt by sourcing /opt/Xilinx/14.7/ISE_DS/.settings64.sh


    kees@nb-kjongenburger:/opt/Xilinx/14.7/ISE_DS$ . settings64.sh 
    . /opt/Xilinx/14.7/ISE_DS/common/.settings64.sh /opt/Xilinx/14.7/ISE_DS/common
    . /opt/Xilinx/14.7/ISE_DS/EDK/.settings64.sh /opt/Xilinx/14.7/ISE_DS/EDK
    . /opt/Xilinx/14.7/ISE_DS/PlanAhead/.settings64.sh /opt/Xilinx/14.7/ISE_DS/PlanAhead
    . /opt/Xilinx/14.7/ISE_DS/ISE/.settings64.sh /opt/Xilinx/14.7/ISE_DS/ISE


Next you need to make sure the openadc is also checkout at it contains the makeise scipts to generated configuration files for the ise IDE

Onece this is done you can execute makeise in the following folder

    ~/projects/chipwhisperer/hardware/capture/chipwhisperer-lite/hdl$ ../../../../openadc/hdl/makeise/makeise.py cwlite.in 
    Using cwlite.in input file to make cwlite.xise

    FPGA = Spartan6 xc6slx9 in tqg144-3
    **Verilog Sources:
       cwlite_ise/cwlite_interface.v
       ../../../common/hdl/reg_main_cwlite.v
       setup.v
       ../../../../openadc/hdl/hdl/openadc_interface.v
       ../../../../openadc/hdl/hdl/reg_openadc.v
       ../../../../openadc/hdl/hdl/reg_openadc_adcfifo.v
       ../../../../openadc/hdl/hdl/trigger_unit.v
       ../../../../openadc/hdl/hdl/spartan6/dcm_phaseshift_interface.v
       ../../../../openadc/hdl/hdl/spartan6/clock_managment_advanced.v
       ../../../../openadc/hdl/hdl/spartan6/dcm_clkgen_load.v
       ../../../common/hdl/clockglitch/clockglitch_s6.v
       ../../../common/hdl/clockglitch/reg_clockglitch.v
       ../../../common/hdl/clockglitch/trigger_resync.v
       ../../../common/hdl/io_trigger/reg_iotrigger.v
       ../../../common/hdl/io_trigger/trigger_system.v
       ../../../common/hdl/reg_chipwhisperer.v
       ../../../common/hdl/reconfig/reg_reconfig.v
       ../../../common/hdl/fifo_stream/fifo_top_stream.v
    **UCF Files:
       cwlite_ise/cwlite_lx9_tqfp144.ucf
    **XCO Files:
       fifoonly_adcfifo.xco
       icap_fifo.xco


and open the file ise ise cwlite.xise.

In the design tab select "generate programming file" to compile the HDL code. You will be prompted to launch the IP core generator twice during this process.


()[pics/generate_ip01.png]



Partial reconfig(to hard to guess)

https://www.xilinx.com/support/documentation/sw_manuals/xilinx14_4/PlanAhead_Tutorial_Partial_Reconfiguration.pdf



