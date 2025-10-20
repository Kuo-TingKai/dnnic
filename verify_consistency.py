#!/usr/bin/env python3
"""
Simplified Software-Hardware Consistency Verification
Direct comparison of software DNN calculations with hardware DNN logic
"""

import numpy as np
import torch
import json

def software_dnn_forward(inputs, weights_layer1, bias_layer1, weights_layer2, bias_layer2):
    """Software DNN forward pass"""
    
    # Convert to numpy arrays
    inputs = np.array(inputs)
    weights_layer1 = np.array(weights_layer1)
    bias_layer1 = np.array(bias_layer1)
    weights_layer2 = np.array(weights_layer2)
    bias_layer2 = np.array(bias_layer2)
    
    # Layer 1: 4 inputs -> 3 hidden neurons
    # weights_layer1 shape is (3, 4), so we need to transpose for dot product
    hidden = np.dot(inputs, weights_layer1.T) + bias_layer1
    hidden = np.maximum(0, hidden)  # ReLU activation
    
    # Layer 2: 3 hidden neurons -> 2 outputs
    # weights_layer2 shape is (2, 3), so we need to transpose for dot product
    outputs = np.dot(hidden, weights_layer2.T) + bias_layer2
    
    return outputs

def hardware_dnn_forward(inputs, weights_layer1, bias_layer1, weights_layer2, bias_layer2):
    """Hardware DNN forward pass simulation"""
    
    # Convert to numpy arrays
    inputs = np.array(inputs)
    weights_layer1 = np.array(weights_layer1)
    bias_layer1 = np.array(bias_layer1)
    weights_layer2 = np.array(weights_layer2)
    bias_layer2 = np.array(bias_layer2)
    
    # Simulate hardware MAC operations
    # Layer 1 computation
    hidden = np.zeros(3)
    for neuron in range(3):
        # MAC operation: accumulate input * weight + bias
        mac_result = bias_layer1[neuron]
        for input_idx in range(4):
            mac_result += inputs[input_idx] * weights_layer1[input_idx, neuron]
        hidden[neuron] = max(0, mac_result)  # ReLU
    
    # Layer 2 computation
    outputs = np.zeros(2)
    for neuron in range(2):
        # MAC operation: accumulate hidden * weight + bias
        mac_result = bias_layer2[neuron]
        for input_idx in range(3):
            mac_result += hidden[input_idx] * weights_layer2[input_idx, neuron]
        outputs[neuron] = mac_result
    
    return outputs

def main():
    """Main verification function"""
    
    print("=== Software-Hardware DNN Consistency Verification ===")
    
    # Load parameters
    with open('model_parameters.json', 'r') as f:
        params = json.load(f)
    
    # Load test vectors
    test_vectors = np.load('test_vectors.npy')
    
    print(f"Loaded {len(test_vectors)} test vectors")
    print(f"Parameters loaded from model_parameters.json")
    
    # Extract parameters
    layer1_weights = np.array(params['layer1_weights'])
    layer1_bias = np.array(params['layer1_bias'])
    layer2_weights = np.array(params['layer2_weights'])
    layer2_bias = np.array(params['layer2_bias'])
    
    print("\nLayer 1 weights shape:", layer1_weights.shape)
    print("Layer 1 bias shape:", layer1_bias.shape)
    print("Layer 2 weights shape:", layer2_weights.shape)
    print("Layer 2 bias shape:", layer2_bias.shape)
    
    # Transpose weights to match hardware format
    layer1_weights_hw = layer1_weights.T  # 4x3
    layer2_weights_hw = layer2_weights.T   # 3x2
    
    print("\n=== Running Consistency Tests ===")
    
    all_consistent = True
    max_diff = 0
    
    for i, test_input in enumerate(test_vectors):
        # Software computation
        software_output = software_dnn_forward(
            test_input, layer1_weights, layer1_bias, 
            layer2_weights, layer2_bias
        )
        
        # Hardware computation
        hardware_output = hardware_dnn_forward(
            test_input, layer1_weights_hw, layer1_bias,
            layer2_weights_hw, layer2_bias
        )
        
        # Calculate differences
        diff = np.abs(software_output - hardware_output)
        max_diff_test = np.max(diff)
        max_diff = max(max_diff, max_diff_test)
        
        print(f"\nTest {i+1}:")
        print(f"  Input: {test_input.tolist()}")
        print(f"  Software: [{software_output[0]:8.2f}, {software_output[1]:8.2f}]")
        print(f"  Hardware: [{hardware_output[0]:8.2f}, {hardware_output[1]:8.2f}]")
        print(f"  Difference: [{diff[0]:8.2f}, {diff[1]:8.2f}]")
        
        # Check consistency (allow small numerical differences)
        tolerance = 0.01
        consistent = np.all(diff < tolerance)
        if not consistent:
            all_consistent = False
            print(f"  ❌ FAIL - Difference exceeds tolerance ({tolerance})")
        else:
            print(f"  ✅ PASS - Within tolerance ({tolerance})")
    
    print(f"\n=== Summary ===")
    print(f"Maximum difference across all tests: {max_diff:.6f}")
    
    if all_consistent:
        print("✅ ALL TESTS PASSED - Software and hardware outputs are consistent!")
    else:
        print("❌ SOME TESTS FAILED - Software and hardware outputs differ significantly")
    
    # Save results
    results = {
        'test_vectors': test_vectors.tolist(),
        'max_difference': float(max_diff),
        'all_consistent': all_consistent,
        'tolerance': 0.01,
        'layer1_weights_shape': layer1_weights.shape,
        'layer2_weights_shape': layer2_weights.shape
    }
    
    with open('consistency_verification_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to consistency_verification_results.json")
    
    return all_consistent

if __name__ == "__main__":
    main()
