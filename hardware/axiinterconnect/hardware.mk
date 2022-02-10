ifneq (axiinterconnect,$(filter axiinterconnect, $(HW_MODULES)))

# Add to modules list
HW_MODULES+=axiinterconnect

# Sources
VSRC+=$(AXI_DIR)/submodules/V_AXI/rtl/axi_interconnect.v
VSRC+=$(AXI_DIR)/submodules/V_AXI/rtl/arbiter.v
VSRC+=$(AXI_DIR)/submodules/V_AXI/rtl/priority_encoder.v

endif
