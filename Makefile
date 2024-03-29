AXI_DIR:=.
include ./config.mk

# Default module
MODULE_NAME ?=iob2axi
MODULE_DIR=$(shell find . -name $(MODULE_NAME))

VCD ?=1

defmacro:=-D
incdir:=-I

#icarus verilog simulator
VLOG:=iverilog -W all -g2005-sv

# Defines
ifeq ($(VCD),1)
DEFINE+=$(defmacro)VCD
endif

# Includes
INCLUDE+=$(incdir)$(LIB_DIR)/hardware/include

# Headers
VHDR+=$(LIB_DIR)/hardware/include/iob_lib.vh

VHDR+=ddr_axi_wire.vh \
m_ddr_axi_portmap.vh

# Sources
ifneq ($(MODULE_DIR),)
include $(MODULE_DIR)/hardware.mk
endif

# testbench
VSRC+=$(MODULE_DIR)/$(MODULE_NAME)_tb.v

# AXI RAM
VSRC+=$(V_AXI_DIR)/rtl/axi_ram.v

sim: exists $(VSRC) $(VHDR)
	$(VLOG) $(INCLUDE) $(DEFINE) $(VSRC)
	./a.out

exists:
ifeq ($(MODULE_DIR),)
	$(error "Module $(MODULE_NAME) not found")
endif
	@echo "\n\nSimulating module $(MODULE_NAME)\n\n"

ddr_axi_wire.vh:
	$(AXI_GEN) axi_wire AXI_ADDR_W AXI_DATA_W 'ddr_'

m_ddr_axi_portmap.vh:
	$(AXI_GEN) axi_portmap AXI_ADDR_W AXI_DATA_W 'm_' 'ddr_'

waves: uut.vcd
	gtkwave -a $(MODULE_DIR)/waves.gtkw $< &

clean:
	@rm -f *# *~ a.out uut.vcd *.vh

.PHONY: sim waves clean
