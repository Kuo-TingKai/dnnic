// Complete DNN Accelerator
// This module implements a simple 2-layer neural network accelerator
// Layer 1: 4 inputs -> 3 hidden neurons
// Layer 2: 3 hidden neurons -> 2 outputs
// Uses MAC units for computation and includes control logic

module dnn_accelerator (
    input clk,                    // Clock signal
    input rst_n,                  // Reset signal (active low)
    input start,                  // Start computation signal
    input [7:0] input_data_0,    // Input data 0
    input [7:0] input_data_1,    // Input data 1
    input [7:0] input_data_2,    // Input data 2
    input [7:0] input_data_3,    // Input data 3
    output reg [15:0] output_data_0, // Output data 0
    output reg [15:0] output_data_1, // Output data 1
    output reg done,              // Computation done signal
    output reg valid              // Output valid signal
);

    // Internal signals
    reg [7:0] weights_layer1 [0:11];  // Layer 1 weights (4 inputs × 3 neurons)
    reg [7:0] weights_layer2 [0:5];   // Layer 2 weights (3 neurons × 2 outputs)
    reg [15:0] bias_layer1 [0:2];     // Layer 1 biases (3 neurons)
    reg [15:0] bias_layer2 [0:1];     // Layer 2 biases (2 outputs)
    
    reg [15:0] hidden_layer [0:2];    // Hidden layer activations
    reg [15:0] mac_result;            // MAC computation result
    
    // Control signals
    reg [2:0] state;                  // State machine
    reg [1:0] neuron_idx;              // Current neuron index
    reg [1:0] input_idx;               // Current input index
    
    // State machine states
    localparam IDLE = 3'b000;
    localparam LAYER1_COMPUTE = 3'b001;
    localparam LAYER2_COMPUTE = 3'b010;
    localparam DONE_STATE = 3'b100;
    
    // MAC unit instantiation
    wire [7:0] current_input;
    wire [7:0] current_weight;
    wire [15:0] mac_out;
    
    // Multiplexer for input data
    assign current_input = (input_idx == 2'b00) ? input_data_0 :
                          (input_idx == 2'b01) ? input_data_1 :
                          (input_idx == 2'b10) ? input_data_2 : input_data_3;
    
    // Multiplexer for weights
    assign current_weight = (state == LAYER1_COMPUTE) ? 
                           weights_layer1[neuron_idx * 4 + input_idx] :
                           weights_layer2[neuron_idx * 3 + input_idx];
    
    mac_unit mac_inst (
        .A(current_input),
        .W(current_weight),
        .B(mac_result),
        .C(mac_out)
    );
    
    // Initialize weights and biases
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // Initialize weights (simplified values)
            weights_layer1[0] <= 8'd10;  weights_layer1[1] <= 8'd20;  weights_layer1[2] <= 8'd30;  weights_layer1[3] <= 8'd40;
            weights_layer1[4] <= 8'd15;  weights_layer1[5] <= 8'd25;  weights_layer1[6] <= 8'd35;  weights_layer1[7] <= 8'd45;
            weights_layer1[8] <= 8'd12;  weights_layer1[9] <= 8'd22;  weights_layer1[10] <= 8'd32; weights_layer1[11] <= 8'd42;
            
            weights_layer2[0] <= 8'd50;  weights_layer2[1] <= 8'd60;  weights_layer2[2] <= 8'd70;
            weights_layer2[3] <= 8'd55;  weights_layer2[4] <= 8'd65;  weights_layer2[5] <= 8'd75;
            
            // Initialize biases
            bias_layer1[0] <= 16'd100; bias_layer1[1] <= 16'd200; bias_layer1[2] <= 16'd300;
            bias_layer2[0] <= 16'd150; bias_layer2[1] <= 16'd250;
            
            // Initialize control signals
            state <= IDLE;
            neuron_idx <= 0;
            input_idx <= 0;
            mac_result <= 0;
            done <= 0;
            valid <= 0;
        end else begin
            case (state)
                IDLE: begin
                    if (start) begin
                        state <= LAYER1_COMPUTE;
                        neuron_idx <= 0;
                        input_idx <= 0;
                        mac_result <= bias_layer1[0];
                        done <= 0;
                        valid <= 0;
                    end
                end
                
                LAYER1_COMPUTE: begin
                    if (input_idx < 3) begin
                        mac_result <= mac_out;
                        input_idx <= input_idx + 1;
                    end else begin
                        // Store hidden layer result
                        hidden_layer[neuron_idx] <= mac_out;
                        input_idx <= 0;
                        
                        if (neuron_idx < 2) begin
                            neuron_idx <= neuron_idx + 1;
                            mac_result <= bias_layer1[neuron_idx + 1];
                        end else begin
                            // Layer 1 complete, move to layer 2
                            state <= LAYER2_COMPUTE;
                            neuron_idx <= 0;
                            input_idx <= 0;
                            mac_result <= bias_layer2[0];
                        end
                    end
                end
                
                LAYER2_COMPUTE: begin
                    if (input_idx < 2) begin
                        mac_result <= mac_out;
                        input_idx <= input_idx + 1;
                    end else begin
                        // Store output result
                        if (neuron_idx == 0) begin
                            output_data_0 <= mac_out;
                        end else begin
                            output_data_1 <= mac_out;
                        end
                        
                        input_idx <= 0;
                        
                        if (neuron_idx < 1) begin
                            neuron_idx <= neuron_idx + 1;
                            mac_result <= bias_layer2[neuron_idx + 1];
                        end else begin
                            // Computation complete
                            state <= DONE_STATE;
                            done <= 1;
                            valid <= 1;
                        end
                    end
                end
                
                DONE_STATE: begin
                    if (!start) begin
                        state <= IDLE;
                        done <= 0;
                        valid <= 0;
                    end
                end
                
                default: state <= IDLE;
            endcase
        end
    end

endmodule
