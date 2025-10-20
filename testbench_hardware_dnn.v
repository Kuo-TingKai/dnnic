// Hardware DNN Testbench
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
        test_inputs[0] = {70, 120, 201, 51};
        test_inputs[1] = {65, 64, 127, 96};
        test_inputs[2] = {115, 132, 139, 87};
        test_inputs[3] = {74, 88, 95, 87};
        test_inputs[4] = {137, 129, 185, 144};
        test_inputs[5] = {229, 183, 55, 114};
        test_inputs[6] = {167, 197, 145, 143};
        test_inputs[7] = {99, 120, 44, 68};
        test_inputs[8] = {166, 140, 40, 127};
        test_inputs[9] = {50, 0, 141, 255};

        // Expected outputs (scaled from software predictions)
        expected_outputs[0] = {30979, 1787};
        expected_outputs[1] = {22897, 9869};
        expected_outputs[2] = {28832, 3934};
        expected_outputs[3] = {22897, 9869};
        expected_outputs[4] = {22897, 9869};
        expected_outputs[5] = {0, 32766};
        expected_outputs[6] = {2369, 30397};
        expected_outputs[7] = {766, 32000};
        expected_outputs[8] = {1, 32765};
        expected_outputs[9] = {22897, 9869};

        // Reset
        rst_n = 0;
        start = 0;
        #20 rst_n = 1;
        #20;
        
        // Run tests
        $display("=== Hardware DNN Test Results ===");

        // Test case 1
        input_data_0 = test_inputs[0][0];
        input_data_1 = test_inputs[0][1];
        input_data_2 = test_inputs[0][2];
        input_data_3 = test_inputs[0][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 1: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[0][0], expected_outputs[0][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[0][0] - 1000 && 
            output_data_0 <= expected_outputs[0][0] + 1000 &&
            output_data_1 >= expected_outputs[0][1] - 1000 && 
            output_data_1 <= expected_outputs[0][1] + 1000) begin
            $display("Test 1: PASS");
        end else begin
            $display("Test 1: FAIL");
        end
        
        #20;

        // Test case 2
        input_data_0 = test_inputs[1][0];
        input_data_1 = test_inputs[1][1];
        input_data_2 = test_inputs[1][2];
        input_data_3 = test_inputs[1][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 2: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[1][0], expected_outputs[1][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[1][0] - 1000 && 
            output_data_0 <= expected_outputs[1][0] + 1000 &&
            output_data_1 >= expected_outputs[1][1] - 1000 && 
            output_data_1 <= expected_outputs[1][1] + 1000) begin
            $display("Test 2: PASS");
        end else begin
            $display("Test 2: FAIL");
        end
        
        #20;

        // Test case 3
        input_data_0 = test_inputs[2][0];
        input_data_1 = test_inputs[2][1];
        input_data_2 = test_inputs[2][2];
        input_data_3 = test_inputs[2][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 3: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[2][0], expected_outputs[2][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[2][0] - 1000 && 
            output_data_0 <= expected_outputs[2][0] + 1000 &&
            output_data_1 >= expected_outputs[2][1] - 1000 && 
            output_data_1 <= expected_outputs[2][1] + 1000) begin
            $display("Test 3: PASS");
        end else begin
            $display("Test 3: FAIL");
        end
        
        #20;

        // Test case 4
        input_data_0 = test_inputs[3][0];
        input_data_1 = test_inputs[3][1];
        input_data_2 = test_inputs[3][2];
        input_data_3 = test_inputs[3][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 4: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[3][0], expected_outputs[3][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[3][0] - 1000 && 
            output_data_0 <= expected_outputs[3][0] + 1000 &&
            output_data_1 >= expected_outputs[3][1] - 1000 && 
            output_data_1 <= expected_outputs[3][1] + 1000) begin
            $display("Test 4: PASS");
        end else begin
            $display("Test 4: FAIL");
        end
        
        #20;

        // Test case 5
        input_data_0 = test_inputs[4][0];
        input_data_1 = test_inputs[4][1];
        input_data_2 = test_inputs[4][2];
        input_data_3 = test_inputs[4][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 5: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[4][0], expected_outputs[4][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[4][0] - 1000 && 
            output_data_0 <= expected_outputs[4][0] + 1000 &&
            output_data_1 >= expected_outputs[4][1] - 1000 && 
            output_data_1 <= expected_outputs[4][1] + 1000) begin
            $display("Test 5: PASS");
        end else begin
            $display("Test 5: FAIL");
        end
        
        #20;

        // Test case 6
        input_data_0 = test_inputs[5][0];
        input_data_1 = test_inputs[5][1];
        input_data_2 = test_inputs[5][2];
        input_data_3 = test_inputs[5][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 6: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[5][0], expected_outputs[5][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[5][0] - 1000 && 
            output_data_0 <= expected_outputs[5][0] + 1000 &&
            output_data_1 >= expected_outputs[5][1] - 1000 && 
            output_data_1 <= expected_outputs[5][1] + 1000) begin
            $display("Test 6: PASS");
        end else begin
            $display("Test 6: FAIL");
        end
        
        #20;

        // Test case 7
        input_data_0 = test_inputs[6][0];
        input_data_1 = test_inputs[6][1];
        input_data_2 = test_inputs[6][2];
        input_data_3 = test_inputs[6][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 7: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[6][0], expected_outputs[6][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[6][0] - 1000 && 
            output_data_0 <= expected_outputs[6][0] + 1000 &&
            output_data_1 >= expected_outputs[6][1] - 1000 && 
            output_data_1 <= expected_outputs[6][1] + 1000) begin
            $display("Test 7: PASS");
        end else begin
            $display("Test 7: FAIL");
        end
        
        #20;

        // Test case 8
        input_data_0 = test_inputs[7][0];
        input_data_1 = test_inputs[7][1];
        input_data_2 = test_inputs[7][2];
        input_data_3 = test_inputs[7][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 8: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[7][0], expected_outputs[7][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[7][0] - 1000 && 
            output_data_0 <= expected_outputs[7][0] + 1000 &&
            output_data_1 >= expected_outputs[7][1] - 1000 && 
            output_data_1 <= expected_outputs[7][1] + 1000) begin
            $display("Test 8: PASS");
        end else begin
            $display("Test 8: FAIL");
        end
        
        #20;

        // Test case 9
        input_data_0 = test_inputs[8][0];
        input_data_1 = test_inputs[8][1];
        input_data_2 = test_inputs[8][2];
        input_data_3 = test_inputs[8][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 9: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[8][0], expected_outputs[8][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[8][0] - 1000 && 
            output_data_0 <= expected_outputs[8][0] + 1000 &&
            output_data_1 >= expected_outputs[8][1] - 1000 && 
            output_data_1 <= expected_outputs[8][1] + 1000) begin
            $display("Test 9: PASS");
        end else begin
            $display("Test 9: FAIL");
        end
        
        #20;

        // Test case 10
        input_data_0 = test_inputs[9][0];
        input_data_1 = test_inputs[9][1];
        input_data_2 = test_inputs[9][2];
        input_data_3 = test_inputs[9][3];
        start = 1;
        #10 start = 0;
        
        wait(done);
        $display("Test 10: Input=[%d,%d,%d,%d], Output=[%d,%d], Expected=[%d,%d]", 
                 input_data_0, input_data_1, input_data_2, input_data_3,
                 output_data_0, output_data_1,
                 expected_outputs[9][0], expected_outputs[9][1]);
        
        // Check if outputs are within acceptable range
        if (output_data_0 >= expected_outputs[9][0] - 1000 && 
            output_data_0 <= expected_outputs[9][0] + 1000 &&
            output_data_1 >= expected_outputs[9][1] - 1000 && 
            output_data_1 <= expected_outputs[9][1] + 1000) begin
            $display("Test 10: PASS");
        end else begin
            $display("Test 10: FAIL");
        end
        
        #20;

        $display("=== Test Complete ===");
        $finish;
    end
    
endmodule
