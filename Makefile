AXI_DIR:=.

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

# Sources
ifneq ($(MODULE_DIR),)
include $(MODULE_DIR)/hardware.mk
endif

# testbench
VSRC+=$(MODULE_DIR)/$(MODULE_NAME)_tb.v

# AXI RAM
VSRC+=$(AXI_DIR)/submodules/V_AXI/rtl/axi_ram.v

sim: exists $(VSRC) $(VHDR)
	$(VLOG) $(INCLUDE) $(DEFINE) $(VSRC)
	./a.out

exists:
ifeq ($(MODULE_DIR),)
	$(error "Module $(MODULE_NAME) not found")
endif
	@echo "\n\nSimulating module $(MODULE_NAME)\n\n"

waves: uut.vcd
	gtkwave -a $(MODULE_DIR)/waves.gtkw $< &

clean:
	@rm -f *# *~ a.out uut.vcd

.PHONY: sim waves clean
