#!/usr/bin/env python3
"""
Parameter Conversion Tool
Converts software DNN parameters to hardware-compatible format
"""

import json
import numpy as np

def convert_parameters_to_hardware(params_file='model_parameters.json'):
    """Convert software parameters to hardware format"""
    
    with open(params_file, 'r') as f:
        params = json.load(f)
    
    print("=== Parameter Conversion ===")
    
    # Convert layer 1 weights (4x3)
    layer1_weights = np.array(params['layer1_weights'])
    layer1_bias = np.array(params['layer1_bias'])
    
    # Convert layer 2 weights (3x2)
    layer2_weights = np.array(params['layer2_weights'])
    layer2_bias = np.array(params['layer2_bias'])
    
    print("Layer 1 weights (4x3):")
    print(layer1_weights)
    print("Layer 1 bias:")
    print(layer1_bias)
    
    print("\nLayer 2 weights (3x2):")
    print(layer2_weights)
    print("Layer 2 bias:")
    print(layer2_bias)
    
    # Generate Verilog initialization code
    verilog_code = generate_verilog_init(layer1_weights, layer1_bias, 
                                       layer2_weights, layer2_bias)
    
    # Save Verilog code
    with open('hardware_parameters.v', 'w') as f:
        f.write(verilog_code)
    
    print("\nVerilog initialization code saved to hardware_parameters.v")
    
    # Generate testbench data
    generate_testbench_data(params)
    
    return layer1_weights, layer1_bias, layer2_weights, layer2_bias

def generate_verilog_init(layer1_weights, layer1_bias, layer2_weights, layer2_bias):
    """Generate Verilog initialization code"""
    
    verilog = """// Hardware DNN Parameter Initialization
// Generated from software model parameters

// Layer 1 weights (4 inputs × 3 neurons)
"""
    
    # Layer 1 weights (transpose to get 4x3 format)
    layer1_weights_t = layer1_weights.T  # Transpose to get 4x3
    
    verilog += "// weights_layer1[0] = ["
    for i in range(4):
        verilog += f"{layer1_weights_t[i, 0]:4d}"
        if i < 3:
            verilog += ", "
    verilog += "]\n"
    
    verilog += "// weights_layer1[1] = ["
    for i in range(4):
        verilog += f"{layer1_weights_t[i, 1]:4d}"
        if i < 3:
            verilog += ", "
    verilog += "]\n"
    
    verilog += "// weights_layer1[2] = ["
    for i in range(4):
        verilog += f"{layer1_weights_t[i, 2]:4d}"
        if i < 3:
            verilog += ", "
    verilog += "]\n"
    
    # Layer 1 bias
    verilog += "\n// Layer 1 bias\n"
    verilog += f"// bias_layer1[0] = {layer1_bias[0]:5d}\n"
    verilog += f"// bias_layer1[1] = {layer1_bias[1]:5d}\n"
    verilog += f"// bias_layer1[2] = {layer1_bias[2]:5d}\n"
    
    # Layer 2 weights (transpose to get 3x2 format)
    layer2_weights_t = layer2_weights.T  # Transpose to get 3x2
    
    verilog += "\n// Layer 2 weights (3 neurons × 2 outputs)\n"
    verilog += "// weights_layer2[0] = ["
    for i in range(3):
        verilog += f"{layer2_weights_t[i, 0]:4d}"
        if i < 2:
            verilog += ", "
    verilog += "]\n"
    
    verilog += "// weights_layer2[1] = ["
    for i in range(3):
        verilog += f"{layer2_weights_t[i, 1]:4d}"
        if i < 2:
            verilog += ", "
    verilog += "]\n"
    
    # Layer 2 bias
    verilog += "\n// Layer 2 bias\n"
    verilog += f"// bias_layer2[0] = {layer2_bias[0]:5d}\n"
    verilog += f"// bias_layer2[1] = {layer2_bias[1]:5d}\n"
    
    # Generate actual Verilog initialization
    verilog += """
// Actual Verilog initialization code
module hardware_parameter_init (
    output reg [7:0] weights_layer1 [0:11],
    output reg [7:0] weights_layer2 [0:5],
    output reg [15:0] bias_layer1 [0:2],
    output reg [15:0] bias_layer2 [0:1]
);

always @(*) begin
    // Layer 1 weights initialization
"""
    
    # Layer 1 weights
    for i in range(4):
        for j in range(3):
            idx = i * 3 + j
            verilog += f"    weights_layer1[{idx}] = 8'd{layer1_weights_t[i, j] & 0xFF};\n"
    
    verilog += "\n    // Layer 2 weights initialization\n"
    # Layer 2 weights
    for i in range(3):
        for j in range(2):
            idx = i * 2 + j
            verilog += f"    weights_layer2[{idx}] = 8'd{layer2_weights_t[i, j] & 0xFF};\n"
    
    verilog += "\n    // Layer 1 bias initialization\n"
    for i in range(3):
        verilog += f"    bias_layer1[{i}] = 16'd{layer1_bias[i] & 0xFFFF};\n"
    
    verilog += "\n    // Layer 2 bias initialization\n"
    for i in range(2):
        verilog += f"    bias_layer2[{i}] = 16'd{layer2_bias[i] & 0xFFFF};\n"
    
    verilog += "end\n\nendmodule\n"
    
    return verilog

def generate_testbench_data(params):
    """Generate testbench data for hardware verification"""
    
    # Load test vectors
    test_vectors = np.load('test_vectors.npy')
    software_predictions = np.load('software_predictions.npy')
    
    print(f"\nGenerating testbench data for {len(test_vectors)} test vectors...")
    
    # Generate Verilog testbench
    testbench = """// Hardware DNN Testbench
// Generated from software model test vectors

module testbench_hardware_dnn();
    reg clk, rst_n, start;
    reg [7:0] input_data_0, input_data_1, input_data_2, input_data_3;
    wire [15:0] output_data_0, output_data_1;
    wire done, valid;
    
    // Instantiate DNN accelerator
    dnn_accelerator dut (
        .clk(clk),
        .rst_n(rst_n),
        .start(start),
        .input_data_0(input_data_0),
        .input_data_1(input_data_1),
        .input_data_2(input_data_2),
        .input_data_3(input_data_3),
        .output_data_0(output_data_0),
        .output_data_1(output_data_1),
        .done(done),
        .valid(valid)
    );
    
    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    // Test vectors
    reg [7:0] test_inputs [0:9][0:3];
    reg [15:0] expected_outputs [0:9][0:1];
    
    initial begin
        // Initialize test vectors
"""
    
    # Add test vectors
    for i, test_vec in enumerate(test_vectors):
        testbench += f"        test_inputs[{i}] = {{{test_vec[0]}, {test_vec[1]}, {test_vec[2]}, {test_vec[3]}}};\n"
    
    testbench += "\n        // Expected outputs (scaled from software predictions)\n"
    for i, pred in enumerate(software_predictions):
        # Scale predictions to 16-bit range
        scaled_pred = (pred * 32767).astype(np.int16)
        testbench += f"        expected_outputs[{i}] = {{{scaled_pred[0]}, {scaled_pred[1]}}};\n"
    
    testbench += """
        // Reset
        rst_n = 0;
        start = 0;
        #20 rst_n = 1;
        #20;
        
        // Run tests
        $display("=== Hardware DNN Test Results ===");
"""
    
    # Add test cases
    for i in range(len(test_vectors)):
        testbench += f"""
        // Test case {i+1}
        input_data_0 = test_inputs[{i}][0];
        input_data_1 = test_inputs[{i}][1];
        input_data_2 = test_inputs[{i}][2];
        input_data_3 = test_inputs[{i}][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test {i+1}: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[{i}][0], expected_outputs[{i}][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[{i}][0] - 1000 && 
            output_data_0 <= expected_outputs[{i}][0] + 1000 &&
            output_data_1 >= expected_outputs[{i}][1] - 1000 && 
            output_data_1 <= expected_outputs[{i}][1] + 1000) begin
            $display("Test {i+1}: PASS");
        end else begin
            $display("Test {i+1}: FAIL");
        end
        
        #20;
"""
    
    testbench += """
        $display("=== Test Complete ===");
        $finish;
    end
    
endmodule
"""
    
    # Save testbench
    with open('testbench_hardware_dnn.v', 'w') as f:
        f.write(testbench)
    
    print("Testbench saved to testbench_hardware_dnn.v")

def main():
    """Main conversion function"""
    convert_parameters_to_hardware()

if __name__ == "__main__":
    main()
