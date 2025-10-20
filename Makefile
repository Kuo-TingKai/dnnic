# Makefile for cocotb verification
# This file configures cocotb to test our MAC unit and DNN accelerator

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = mac_unit.v dnn_accelerator.v configurable_dnn_accelerator.v
TOPLEVEL = mac_unit
MODULE = test_mac
SIM = verilator

# Include cocotb makefiles
include $(shell cocotb-config --makefiles)/Makefile.sim

# Additional targets for synthesis and FPGA flow
.PHONY: synth clean-all test-dnn synth-dnn test-configurable train-model convert-params test-consistency help

# Synthesis target using Yosys for MAC unit
synth:
	@echo "Running synthesis with Yosys for MAC unit..."
	yosys synth.ys
	@echo "Synthesis complete. Check mac_unit_synth.v for synthesized netlist."

# Synthesis target for DNN accelerator
synth-dnn:
	@echo "Running synthesis with Yosys for DNN accelerator..."
	yosys synth_dnn.ys
	@echo "DNN synthesis complete. Check dnn_accelerator_synth.v for synthesized netlist."

# Synthesis target for configurable DNN accelerator
synth-configurable:
	@echo "Running synthesis with Yosys for configurable DNN accelerator..."
	yosys synth_configurable.ys
	@echo "Configurable DNN synthesis complete. Check configurable_dnn_accelerator_synth.v for synthesized netlist."

# Test DNN accelerator
test-dnn:
	@echo "Testing DNN accelerator..."
	$(MAKE) TOPLEVEL=dnn_accelerator MODULE=test_dnn VERILOG_SOURCES="mac_unit.v dnn_accelerator.v"
	@echo "DNN accelerator tests complete."

# Test configurable DNN accelerator
test-configurable:
	@echo "Testing configurable DNN accelerator..."
	$(MAKE) TOPLEVEL=configurable_dnn_accelerator MODULE=test_configurable_dnn VERILOG_SOURCES="mac_unit.v configurable_dnn_accelerator.v"
	@echo "Configurable DNN accelerator tests complete."

# Train software model
train-model:
	@echo "Training software DNN model..."
	python3 train_software_dnn.py
	@echo "Software model training complete."

# Convert parameters
convert-params:
	@echo "Converting parameters to hardware format..."
	python3 convert_parameters.py
	@echo "Parameter conversion complete."

# Test software-hardware consistency
test-consistency:
	@echo "Testing software-hardware consistency..."
	python3 test_consistency.py
	@echo "Consistency test complete."

# Simplified consistency verification
verify:
	@echo "Running simplified consistency verification..."
	python3 verify_consistency.py
	@echo "Consistency verification complete."

# Full pipeline: train model, convert parameters, test hardware
full-pipeline: train-model convert-params test-configurable test-consistency
	@echo "Full pipeline complete!"

# Clean all generated files
clean-all: clean
	@echo "Cleaning synthesis files..."
	rm -f mac_unit_synth.v mac_unit.json mac_unit.asc mac_unit.bin
	rm -f dnn_accelerator_synth.v dnn_accelerator.json dnn_accelerator.asc dnn_accelerator.bin
	rm -f configurable_dnn_accelerator_synth.v configurable_dnn_accelerator.json
	rm -f model_parameters.json test_vectors.npy software_predictions.npy
	rm -f hardware_parameters.v testbench_hardware_dnn.v
	rm -f hardware_outputs.npy consistency_test_results.json
	@echo "All files cleaned."

# Help target
help:
	@echo "Available targets:"
	@echo "  make                - Run MAC unit cocotb tests"
	@echo "  make test-dnn       - Run DNN accelerator tests"
	@echo "  make test-configurable - Run configurable DNN accelerator tests"
	@echo "  make synth          - Run synthesis for MAC unit"
	@echo "  make synth-dnn      - Run synthesis for DNN accelerator"
	@echo "  make synth-configurable - Run synthesis for configurable DNN accelerator"
	@echo "  make train-model    - Train software DNN model"
	@echo "  make convert-params - Convert parameters to hardware format"
	@echo "  make test-consistency - Test software-hardware consistency"
	@echo "  make full-pipeline  - Run complete training and testing pipeline"
	@echo "  make verify         - Run simplified consistency verification"
	@echo "  make clean          - Clean test files"
	@echo "  make clean-all      - Clean all files including synthesis"
	@echo "  make help           - Show this help"
