# Makefile for cocotb verification
# This file configures cocotb to test our MAC unit

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = mac_unit.v
TOPLEVEL = mac_unit
MODULE = test_mac
SIM = verilator

# Include cocotb makefiles
include $(shell cocotb-config --makefiles)/Makefile.sim

# Additional targets for synthesis and FPGA flow
.PHONY: synth clean-all

# Synthesis target using Yosys
synth:
	@echo "Running synthesis with Yosys..."
	yosys synth.ys
	@echo "Synthesis complete. Check mac_unit_synth.v for synthesized netlist."

# Clean all generated files
clean-all: clean
	@echo "Cleaning synthesis files..."
	rm -f mac_unit_synth.v mac_unit.json mac_unit.asc mac_unit.bin
	@echo "All files cleaned."

# Help target
help:
	@echo "Available targets:"
	@echo "  make          - Run cocotb tests"
	@echo "  make synth    - Run synthesis with Yosys"
	@echo "  make clean    - Clean test files"
	@echo "  make clean-all- Clean all files including synthesis"
	@echo "  make help     - Show this help"
