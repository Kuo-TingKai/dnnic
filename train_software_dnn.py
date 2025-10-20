#!/usr/bin/env python3
"""
Software DNN Training Script
This script trains a small neural network and exports parameters for hardware implementation
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json
import os

class SimpleDNN(nn.Module):
    """Simple 2-layer neural network matching our hardware architecture"""
    
    def __init__(self, input_size=4, hidden_size=3, output_size=2):
        super(SimpleDNN, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.layer2(x)
        return x

def generate_synthetic_data(n_samples=1000, n_features=4, n_classes=2):
    """Generate synthetic classification data"""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_redundant=0,
        n_informative=n_features,
        n_clusters_per_class=1,
        n_classes=n_classes,
        random_state=42
    )
    
    # Scale features to 0-255 range (8-bit)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = (X_scaled - X_scaled.min()) / (X_scaled.max() - X_scaled.min())
    X_scaled = (X_scaled * 255).astype(np.uint8)
    
    return X_scaled, y

def train_model():
    """Train the neural network model"""
    print("Generating synthetic data...")
    X, y = generate_synthetic_data()
    
    # Convert to PyTorch tensors
    X_tensor = torch.FloatTensor(X)
    y_tensor = torch.LongTensor(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_tensor, y_tensor, test_size=0.2, random_state=42
    )
    
    # Create model
    model = SimpleDNN(input_size=4, hidden_size=3, output_size=2)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    print("Training model...")
    # Training loop
    epochs = 100
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
    
    # Test accuracy
    with torch.no_grad():
        test_outputs = model(X_test)
        _, predicted = torch.max(test_outputs.data, 1)
        accuracy = (predicted == y_test).sum().item() / y_test.size(0)
        print(f'Test Accuracy: {accuracy:.4f}')
    
    return model, X_test, y_test

def extract_parameters(model):
    """Extract model parameters for hardware implementation"""
    params = {}
    
    # Extract weights and biases
    with torch.no_grad():
        # Layer 1 weights (4x3)
        layer1_weights = model.layer1.weight.data.numpy()
        layer1_bias = model.layer1.bias.data.numpy()
        
        # Layer 2 weights (3x2)
        layer2_weights = model.layer2.weight.data.numpy()
        layer2_bias = model.layer2.bias.data.numpy()
        
        # Convert to 8-bit integers for hardware
        # Scale weights to fit in 8-bit range
        layer1_weights_scaled = (layer1_weights * 127).astype(np.int8)
        layer1_bias_scaled = (layer1_bias * 127).astype(np.int16)
        
        layer2_weights_scaled = (layer2_weights * 127).astype(np.int8)
        layer2_bias_scaled = (layer2_bias * 127).astype(np.int16)
        
        params['layer1_weights'] = layer1_weights_scaled.tolist()
        params['layer1_bias'] = layer1_bias_scaled.tolist()
        params['layer2_weights'] = layer2_weights_scaled.tolist()
        params['layer2_bias'] = layer2_bias_scaled.tolist()
        
        # Also store original floating point values for comparison
        params['layer1_weights_fp'] = layer1_weights.tolist()
        params['layer1_bias_fp'] = layer1_bias.tolist()
        params['layer2_weights_fp'] = layer2_weights.tolist()
        params['layer2_bias_fp'] = layer2_bias.tolist()
    
    return params

def save_parameters(params, filename='model_parameters.json'):
    """Save parameters to JSON file"""
    with open(filename, 'w') as f:
        json.dump(params, f, indent=2)
    print(f"Parameters saved to {filename}")

def generate_test_vectors(n_samples=10):
    """Generate test vectors for hardware verification"""
    X, _ = generate_synthetic_data(n_samples=n_samples)
    return X

def main():
    """Main training function"""
    print("=== Software DNN Training ===")
    
    # Train model
    model, X_test, y_test = train_model()
    
    # Extract parameters
    print("\nExtracting parameters...")
    params = extract_parameters(model)
    
    # Save parameters
    save_parameters(params)
    
    # Generate test vectors
    print("\nGenerating test vectors...")
    test_vectors = generate_test_vectors(10)
    
    # Save test vectors
    np.save('test_vectors.npy', test_vectors)
    print("Test vectors saved to test_vectors.npy")
    
    # Test software model on test vectors
    print("\nSoftware model predictions:")
    with torch.no_grad():
        test_tensor = torch.FloatTensor(test_vectors)
        software_outputs = model(test_tensor)
        software_predictions = torch.softmax(software_outputs, dim=1)
        
        for i, (input_vec, pred) in enumerate(zip(test_vectors, software_predictions)):
            print(f"Test {i+1}: Input={input_vec.tolist()}, Output={pred.numpy().tolist()}")
    
    # Save software predictions for comparison
    np.save('software_predictions.npy', software_predictions.numpy())
    print("\nSoftware predictions saved to software_predictions.npy")
    
    print("\n=== Training Complete ===")
    print("Files generated:")
    print("- model_parameters.json: Model weights and biases")
    print("- test_vectors.npy: Test input vectors")
    print("- software_predictions.npy: Software model predictions")

if __name__ == "__main__":
    main()
