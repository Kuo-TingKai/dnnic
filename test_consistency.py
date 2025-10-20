#!/usr/bin/env python3
"""
Software-Hardware Consistency Test
Compares software DNN predictions with hardware DNN outputs
"""

import numpy as np
import torch
import json
import subprocess
import os
import time

class SoftwareDNN:
    """Software DNN model for comparison"""
    
    def __init__(self, params_file='model_parameters.json'):
        with open(params_file, 'r') as f:
            self.params = json.load(f)
        
        # Create model
        self.model = torch.nn.Sequential(
            torch.nn.Linear(4, 3),
            torch.nn.ReLU(),
            torch.nn.Linear(3, 2)
        )
        
        # Load parameters
        self.load_parameters()
    
    def load_parameters(self):
        """Load parameters from JSON file"""
        with torch.no_grad():
            # Layer 1
            layer1_weight = torch.tensor(self.params['layer1_weights_fp'], dtype=torch.float32)
            layer1_bias = torch.tensor(self.params['layer1_bias_fp'], dtype=torch.float32)
            self.model[0].weight.data = layer1_weight
            self.model[0].bias.data = layer1_bias
            
            # Layer 2
            layer2_weight = torch.tensor(self.params['layer2_weights_fp'], dtype=torch.float32)
            layer2_bias = torch.tensor(self.params['layer2_bias_fp'], dtype=torch.float32)
            self.model[2].weight.data = layer2_weight
            self.model[2].bias.data = layer2_bias
    
    def predict(self, inputs):
        """Make predictions on input data"""
        with torch.no_grad():
            inputs_tensor = torch.FloatTensor(inputs)
            outputs = self.model(inputs_tensor)
            return outputs.numpy()

def run_hardware_simulation(test_vectors, params):
    """Run hardware simulation and extract outputs"""
    
    print("Running hardware simulation...")
    
    # Generate Verilog testbench with actual test vectors
    generate_hardware_testbench(test_vectors, params)
    
    # Run simulation using cocotb
    try:
        # Set up environment
        env = os.environ.copy()
        env['COCOTB_TEST_MODULES'] = 'test_configurable_dnn'
        env['COCOTB_TOPLEVEL'] = 'configurable_dnn_accelerator'
        env['VERILOG_SOURCES'] = 'mac_unit.v configurable_dnn_accelerator.v'
        
        # Run simulation
        result = subprocess.run(['make', 'test-configurable'], 
                              capture_output=True, text=True, env=env)
        
        if result.returncode != 0:
            print("Hardware simulation failed:")
            print(result.stderr)
            return None
        
        # Parse simulation output
        hardware_outputs = parse_simulation_output(result.stdout)
        return hardware_outputs
        
    except Exception as e:
        print(f"Error running hardware simulation: {e}")
        return None

def generate_hardware_testbench(test_vectors, params):
    """Generate Verilog testbench for hardware simulation"""
    
    testbench = """import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.clock import Clock
import numpy as np

@cocotb.test()
async def test_configurable_dnn_consistency(dut):
    \"\"\"Test configurable DNN accelerator with software-trained parameters\"\"\"
    
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the design
    dut.rst_n.value = 0
    dut.start.value = 0
    dut.load_params.value = 0
    await Timer(20, unit="ns")
    dut.rst_n.value = 1
    await Timer(20, unit="ns")
    
    # Load parameters
    print("Loading parameters...")
    dut.load_params.value = 1
    
    # Layer 1 weights
    layer1_weights = """ + str(params['layer1_weights']) + """
    for i, weight in enumerate(layer1_weights):
        dut.param_addr.value = i
        dut.param_data.value = weight & 0xFF
        dut.param_valid.value = 1
        await RisingEdge(dut.clk)
        dut.param_valid.value = 0
        await RisingEdge(dut.clk)
    
    # Layer 2 weights
    layer2_weights = """ + str(params['layer2_weights']) + """
    for i, weight in enumerate(layer2_weights):
        dut.param_addr.value = i + 12
        dut.param_data.value = weight & 0xFF
        dut.param_valid.value = 1
        await RisingEdge(dut.clk)
        dut.param_valid.value = 0
        await RisingEdge(dut.clk)
    
    # Layer 1 bias
    layer1_bias = """ + str(params['layer1_bias']) + """
    for i, bias in enumerate(layer1_bias):
        # Low byte
        dut.param_addr.value = 18 + i * 2
        dut.param_data.value = bias & 0xFF
        dut.param_valid.value = 1
        await RisingEdge(dut.clk)
        dut.param_valid.value = 0
        await RisingEdge(dut.clk)
        # High byte
        dut.param_addr.value = 18 + i * 2 + 1
        dut.param_data.value = (bias >> 8) & 0xFF
        dut.param_valid.value = 1
        await RisingEdge(dut.clk)
        dut.param_valid.value = 0
        await RisingEdge(dut.clk)
    
    # Layer 2 bias
    layer2_bias = """ + str(params['layer2_bias']) + """
    for i, bias in enumerate(layer2_bias):
        # Low byte
        dut.param_addr.value = 21 + i * 2
        dut.param_data.value = bias & 0xFF
        dut.param_valid.value = 1
        await RisingEdge(dut.clk)
        dut.param_valid.value = 0
        await RisingEdge(dut.clk)
        # High byte
        dut.param_addr.value = 21 + i * 2 + 1
        dut.param_data.value = (bias >> 8) & 0xFF
        dut.param_valid.value = 1
        await RisingEdge(dut.clk)
        dut.param_valid.value = 0
        await RisingEdge(dut.clk)
    
    dut.load_params.value = 0
    await RisingEdge(dut.clk)
    
    # Test vectors
    test_vectors = """ + str(test_vectors.tolist()) + """
    
    print("Running hardware tests...")
    hardware_outputs = []
    
    for i, test_vec in enumerate(test_vectors):
        # Set input data
        dut.input_data_0.value = int(test_vec[0])
        dut.input_data_1.value = int(test_vec[1])
        dut.input_data_2.value = int(test_vec[2])
        dut.input_data_3.value = int(test_vec[3])
        
        # Start computation
        dut.start.value = 1
        await RisingEdge(dut.clk)
        dut.start.value = 0
        
        # Wait for completion
        while not dut.done.value:
            await RisingEdge(dut.clk)
        
        # Record outputs
        output_0 = dut.output_data_0.value.integer
        output_1 = dut.output_data_1.value.integer
        hardware_outputs.append([output_0, output_1])
        
        print(f"Hardware Test {i+1}: Input={test_vec.tolist()}, Output=[{output_0}, {output_1}]")
        
        # Wait for done signal to be deasserted
        while dut.done.value:
            await RisingEdge(dut.clk)
    
    # Save hardware outputs
    np.save('hardware_outputs.npy', np.array(hardware_outputs))
    print("Hardware outputs saved to hardware_outputs.npy")
"""
    
    with open('test_configurable_dnn.py', 'w') as f:
        f.write(testbench)

def parse_simulation_output(output):
    """Parse simulation output to extract hardware results"""
    # This is a simplified parser - in practice, you'd parse the actual simulation output
    # For now, we'll load from the saved file
    try:
        return np.load('hardware_outputs.npy')
    except FileNotFoundError:
        return None

def compare_outputs(software_outputs, hardware_outputs):
    """Compare software and hardware outputs"""
    
    print("\n=== Software-Hardware Comparison ===")
    
    if hardware_outputs is None:
        print("Hardware simulation failed - cannot compare")
        return False
    
    # Scale software outputs to match hardware range
    software_scaled = software_outputs * 32767  # Scale to 16-bit range
    
    print(f"Software outputs shape: {software_scaled.shape}")
    print(f"Hardware outputs shape: {hardware_outputs.shape}")
    
    # Calculate differences
    diff_0 = np.abs(software_scaled[:, 0] - hardware_outputs[:, 0])
    diff_1 = np.abs(software_scaled[:, 1] - hardware_outputs[:, 1])
    
    print("\nOutput differences:")
    for i in range(len(software_scaled)):
        print(f"Test {i+1}:")
        print(f"  Software: [{software_scaled[i, 0]:8.1f}, {software_scaled[i, 1]:8.1f}]")
        print(f"  Hardware: [{hardware_outputs[i, 0]:8d}, {hardware_outputs[i, 1]:8d}]")
        print(f"  Diff:     [{diff_0[i]:8.1f}, {diff_1[i]:8.1f}]")
    
    # Check if differences are within acceptable range
    tolerance = 1000  # Allow 1000 units difference
    max_diff_0 = np.max(diff_0)
    max_diff_1 = np.max(diff_1)
    
    print(f"\nMaximum differences:")
    print(f"  Output 0: {max_diff_0:.1f}")
    print(f"  Output 1: {max_diff_1:.1f}")
    print(f"  Tolerance: {tolerance}")
    
    consistent = (max_diff_0 < tolerance) and (max_diff_1 < tolerance)
    
    if consistent:
        print("\n✅ CONSISTENCY TEST PASSED")
        print("Software and hardware outputs are within acceptable range")
    else:
        print("\n❌ CONSISTENCY TEST FAILED")
        print("Software and hardware outputs differ significantly")
    
    return consistent

def main():
    """Main consistency test function"""
    
    print("=== Software-Hardware DNN Consistency Test ===")
    
    # Load test vectors
    test_vectors = np.load('test_vectors.npy')
    print(f"Loaded {len(test_vectors)} test vectors")
    
    # Load parameters
    with open('model_parameters.json', 'r') as f:
        params = json.load(f)
    
    # Create software model
    print("\nCreating software model...")
    software_model = SoftwareDNN()
    
    # Get software predictions
    print("Running software predictions...")
    software_outputs = software_model.predict(test_vectors)
    
    # Run hardware simulation
    print("\nRunning hardware simulation...")
    hardware_outputs = run_hardware_simulation(test_vectors, params)
    
    # Compare outputs
    consistent = compare_outputs(software_outputs, hardware_outputs)
    
    # Save results
    results = {
        'test_vectors': test_vectors.tolist(),
        'software_outputs': software_outputs.tolist(),
        'hardware_outputs': hardware_outputs.tolist() if hardware_outputs is not None else None,
        'consistent': consistent,
        'timestamp': time.time()
    }
    
    with open('consistency_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to consistency_test_results.json")
    
    return consistent

if __name__ == "__main__":
    main()
