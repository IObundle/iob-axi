LIB_DIR:=../..

VCD ?=1

defmacro:=-D
incdir:=-I

#icarus verilog simulator
VLOG:=iverilog -W all -g2005-sv

include ./hardware.mk

ifeq ($(VCD),1)
DEFINE+=$(defmacro)VCD
endif

# Includes
INCLUDE+=$(incdir)../include

# Add testbench
VSRC+=iob2axi_tb.v

# Add AXI RAM
VSRC+=$(LIB_DIR)/submodules/AXI/rtl/axi_ram.v

sim: $(VSRC) $(VHDR)
	$(VLOG) $(INCLUDE) $(DEFINE) $(VSRC)
	./a.out

sim-waves: uut.vcd
	gtkwave -a waves.gtkw $< &

clean:
	@rm -f a.out *~ uut.vcd

.PHONY: sim sim-waves clean
