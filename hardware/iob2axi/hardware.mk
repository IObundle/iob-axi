ifneq (iob2axi,$(filter iob2axi, $(HW_MODULES)))

# Add to modules list
HW_MODULES+=iob2axi

# Includes
INCLUDE+=$(incdir)$(AXI_DIR)/hardware/include

# Sources
VSRC+=$(AXI_DIR)/hardware/iob2axi/iob2axi.v \
$(AXI_DIR)/hardware/iob2axi/iob2axi_wr.v \
$(AXI_DIR)/hardware/iob2axi/iob2axi_rd.v

endif
