// Simple MAC (Multiply-Accumulate) Unit for DNN
// This is the core building block of any DNN accelerator
// Function: C = A * W + B

module mac_unit (
    input [7:0] A,    // Input A (8-bit)
    input [7:0] W,    // Weight W (8-bit)
    input [15:0] B,   // Bias B or previous accumulated value (16-bit)
    output [15:0] C   // Output C (accumulated result, 16-bit)
);

    // Multiplier output: 8-bit × 8-bit = 16-bit
    wire [15:0] product; 
    
    // Perform multiplication
    assign product = A * W; 
    
    // Perform accumulation
    assign C = product + B; 

endmodule
