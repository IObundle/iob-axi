ifneq (axiram,$(filter axiram, $(HW_MODULES)))

# Add to modules list
HW_MODULES+=axiram

# Sources
VSRC+=$(AXI_DIR)/submodules/V_AXI/rtl/axi_ram.v

endif
