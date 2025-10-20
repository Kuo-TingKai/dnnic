// Hardware DNN Parameter Initialization
// Generated from software model parameters

// Layer 1 weights (4 inputs × 3 neurons)
// weights_layer1[0] = [  26,   22,    1,  -59]
// weights_layer1[1] = [  58,   15,  -53,  -16]
// weights_layer1[2] = [  -2,  -40,   27,  -61]

// Layer 1 bias
// bias_layer1[0] =     5
// bias_layer1[1] =    -2
// bias_layer1[2] =   -42

// Layer 2 weights (3 neurons × 2 outputs)
// weights_layer2[0] = [  63,   13,   -1]
// weights_layer2[1] = [  44,   36,  -15]

// Layer 2 bias
// bias_layer2[0] =    59
// bias_layer2[1] =   -47

// Actual Verilog initialization code
module hardware_parameter_init (
    output reg [7:0] weights_layer1 [0:11],
    output reg [7:0] weights_layer2 [0:5],
    output reg [15:0] bias_layer1 [0:2],
    output reg [15:0] bias_layer2 [0:1]
);

always @(*) begin
    // Layer 1 weights initialization
    weights_layer1[0] = 8'd26;
    weights_layer1[1] = 8'd58;
    weights_layer1[2] = 8'd254;
    weights_layer1[3] = 8'd22;
    weights_layer1[4] = 8'd15;
    weights_layer1[5] = 8'd216;
    weights_layer1[6] = 8'd1;
    weights_layer1[7] = 8'd203;
    weights_layer1[8] = 8'd27;
    weights_layer1[9] = 8'd197;
    weights_layer1[10] = 8'd240;
    weights_layer1[11] = 8'd195;

    // Layer 2 weights initialization
    weights_layer2[0] = 8'd63;
    weights_layer2[1] = 8'd44;
    weights_layer2[2] = 8'd13;
    weights_layer2[3] = 8'd36;
    weights_layer2[4] = 8'd255;
    weights_layer2[5] = 8'd241;

    // Layer 1 bias initialization
    bias_layer1[0] = 16'd5;
    bias_layer1[1] = 16'd65534;
    bias_layer1[2] = 16'd65494;

    // Layer 2 bias initialization
    bias_layer2[0] = 16'd59;
    bias_layer2[1] = 16'd65489;
end

endmodule
