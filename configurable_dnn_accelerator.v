// Configurable DNN Accelerator
// This module implements a 2-layer neural network accelerator with configurable parameters
// Layer 1: 4 inputs -> 3 hidden neurons
// Layer 2: 3 hidden neurons -> 2 outputs
// Parameters can be loaded from external source

module configurable_dnn_accelerator (
    input clk,                    // Clock signal
    input rst_n,                  // Reset signal (active low)
    input start,                  // Start computation signal
    input load_params,            // Load parameters signal
    input [7:0] param_data,      // Parameter data input
    input [3:0] param_addr,      // Parameter address
    input param_valid,            // Parameter data valid
    input [7:0] input_data_0,    // Input data 0
    input [7:0] input_data_1,    // Input data 1
    input [7:0] input_data_2,    // Input data 2
    input [7:0] input_data_3,    // Input data 3
    output reg [15:0] output_data_0, // Output data 0
    output reg [15:0] output_data_1, // Output data 1
    output reg done,              // Computation done signal
    output reg valid,             // Output valid signal
    output reg params_loaded      // Parameters loaded signal
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
    reg [4:0] param_load_addr;         // Parameter loading address (5 bits for values up to 23)
    
    // State machine states
    localparam IDLE = 3'b000;
    localparam LOAD_PARAMS = 3'b001;
    localparam LAYER1_COMPUTE = 3'b010;
    localparam LAYER2_COMPUTE = 3'b011;
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
    
    // Parameter loading and computation control
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // Initialize control signals
            state <= IDLE;
            neuron_idx <= 0;
            input_idx <= 0;
            mac_result <= 0;
            done <= 0;
            valid <= 0;
            params_loaded <= 0;
            param_load_addr <= 0;
        end else begin
            case (state)
                IDLE: begin
                    if (load_params) begin
                        state <= LOAD_PARAMS;
                        param_load_addr <= 0;
                        params_loaded <= 0;
                    end else if (start && params_loaded) begin
                        state <= LAYER1_COMPUTE;
                        neuron_idx <= 0;
                        input_idx <= 0;
                        mac_result <= bias_layer1[0];
                        done <= 0;
                        valid <= 0;
                    end
                end
                
                LOAD_PARAMS: begin
                    if (param_valid) begin
                        // Load parameters based on address
                        if (param_load_addr < 12) begin
                            // Layer 1 weights
                            weights_layer1[param_load_addr[3:0]] <= param_data;
                        end else if (param_load_addr < 18) begin
                            // Layer 2 weights
                            weights_layer2[param_load_addr[3:0] - 12] <= param_data;
                        end else if (param_load_addr < 21) begin
                            // Layer 1 bias (16-bit, need 2 cycles)
                            if (param_load_addr[0] == 0) begin
                                bias_layer1[param_load_addr[3:1] - 9][7:0] <= param_data;
                            end else begin
                                bias_layer1[param_load_addr[3:1] - 9][15:8] <= param_data;
                            end
                        end else if (param_load_addr < 23) begin
                            // Layer 2 bias (16-bit, need 2 cycles)
                            if (param_load_addr[0] == 0) begin
                                bias_layer2[param_load_addr[3:1] - 10][7:0] <= param_data;
                            end else begin
                                bias_layer2[param_load_addr[3:1] - 10][15:8] <= param_data;
                            end
                        end
                        
                        param_load_addr <= param_load_addr + 1;
                        
                        // Check if all parameters loaded
                        if (param_load_addr >= 22) begin
                            state <= IDLE;
                            params_loaded <= 1;
                        end
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
