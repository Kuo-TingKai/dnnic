import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.clock import Clock
import random

@cocotb.test()
async def dnn_test_basic_functionality(dut):
    """Test basic DNN accelerator functionality"""
    
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the design
    dut.rst_n.value = 0
    dut.start.value = 0
    await Timer(20, unit="ns")
    dut.rst_n.value = 1
    await Timer(20, unit="ns")
    
    # Set input data
    dut.input_data_0.value = 10
    dut.input_data_1.value = 20
    dut.input_data_2.value = 30
    dut.input_data_3.value = 40
    
    # Start computation
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0
    
    # Wait for computation to complete
    while not dut.done.value:
        await RisingEdge(dut.clk)
    
    # Check that valid signal is asserted
    assert dut.valid.value == 1, "Valid signal should be asserted when done"
    
    # Log the results
    dut._log.info(f"DNN Output 0: {dut.output_data_0.value}")
    dut._log.info(f"DNN Output 1: {dut.output_data_1.value}")
    
    # Basic sanity check - outputs should be non-zero
    assert dut.output_data_0.value != 0, "Output 0 should be non-zero"
    assert dut.output_data_1.value != 0, "Output 1 should be non-zero"

@cocotb.test()
async def dnn_test_multiple_computations(dut):
    """Test multiple computations with different inputs"""
    
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the design
    dut.rst_n.value = 0
    dut.start.value = 0
    await Timer(20, unit="ns")
    dut.rst_n.value = 1
    await Timer(20, unit="ns")
    
    # Test case 1: Small values
    dut.input_data_0.value = 1
    dut.input_data_1.value = 2
    dut.input_data_2.value = 3
    dut.input_data_3.value = 4
    
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0
    
    while not dut.done.value:
        await RisingEdge(dut.clk)
    
    output1_0 = dut.output_data_0.value
    output1_1 = dut.output_data_1.value
    dut._log.info(f"Test 1 - Output 0: {output1_0}, Output 1: {output1_1}")
    
    # Wait for done signal to be deasserted
    while dut.done.value:
        await RisingEdge(dut.clk)
    
    # Test case 2: Larger values
    dut.input_data_0.value = 50
    dut.input_data_1.value = 60
    dut.input_data_2.value = 70
    dut.input_data_3.value = 80
    
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0
    
    while not dut.done.value:
        await RisingEdge(dut.clk)
    
    output2_0 = dut.output_data_0.value
    output2_1 = dut.output_data_1.value
    dut._log.info(f"Test 2 - Output 0: {output2_0}, Output 1: {output2_1}")
    
    # Verify outputs are different for different inputs
    assert output1_0 != output2_0, "Outputs should be different for different inputs"
    assert output1_1 != output2_1, "Outputs should be different for different inputs"

@cocotb.test()
async def dnn_test_state_machine(dut):
    """Test DNN accelerator state machine behavior"""
    
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the design
    dut.rst_n.value = 0
    dut.start.value = 0
    await Timer(20, unit="ns")
    dut.rst_n.value = 1
    await Timer(20, unit="ns")
    
    # Initially should be in IDLE state
    assert dut.done.value == 0, "Should be in IDLE state initially"
    assert dut.valid.value == 0, "Valid should be low initially"
    
    # Set input data
    dut.input_data_0.value = 5
    dut.input_data_1.value = 10
    dut.input_data_2.value = 15
    dut.input_data_3.value = 20
    
    # Start computation
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0
    
    # Should not be done immediately
    assert dut.done.value == 0, "Should not be done immediately after start"
    
    # Wait for computation to complete
    cycle_count = 0
    while not dut.done.value and cycle_count < 100:
        await RisingEdge(dut.clk)
        cycle_count += 1
    
    # Should complete within reasonable time
    assert cycle_count < 100, f"Computation took too long: {cycle_count} cycles"
    assert dut.done.value == 1, "Should be done after computation"
    assert dut.valid.value == 1, "Valid should be asserted when done"
    
    dut._log.info(f"Computation completed in {cycle_count} cycles")

@cocotb.test()
async def dnn_test_edge_cases(dut):
    """Test DNN accelerator with edge cases"""
    
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the design
    dut.rst_n.value = 0
    dut.start.value = 0
    await Timer(20, unit="ns")
    dut.rst_n.value = 1
    await Timer(20, unit="ns")
    
    # Test case 1: All zeros
    dut.input_data_0.value = 0
    dut.input_data_1.value = 0
    dut.input_data_2.value = 0
    dut.input_data_3.value = 0
    
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0
    
    while not dut.done.value:
        await RisingEdge(dut.clk)
    
    # With zero inputs, outputs should equal biases
    output_0_zero = dut.output_data_0.value
    output_1_zero = dut.output_data_1.value
    dut._log.info(f"Zero inputs - Output 0: {output_0_zero}, Output 1: {output_1_zero}")
    
    # Wait for reset
    while dut.done.value:
        await RisingEdge(dut.clk)
    
    # Test case 2: Maximum values
    dut.input_data_0.value = 255
    dut.input_data_1.value = 255
    dut.input_data_2.value = 255
    dut.input_data_3.value = 255
    
    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0
    
    while not dut.done.value:
        await RisingEdge(dut.clk)
    
    output_0_max = dut.output_data_0.value
    output_1_max = dut.output_data_1.value
    dut._log.info(f"Max inputs - Output 0: {output_0_max}, Output 1: {output_1_max}")
    
    # Max inputs should produce larger outputs than zero inputs
    assert output_0_max.integer > output_0_zero.integer, "Max inputs should produce larger output than zero inputs"
    assert output_1_max.integer > output_1_zero.integer, "Max inputs should produce larger output than zero inputs"

@cocotb.test()
async def dnn_test_random_inputs(dut):
    """Test DNN accelerator with random inputs"""
    
    # Start clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the design
    dut.rst_n.value = 0
    dut.start.value = 0
    await Timer(20, unit="ns")
    dut.rst_n.value = 1
    await Timer(20, unit="ns")
    
    # Test with multiple random input sets
    for i in range(5):
        # Generate random inputs
        inputs = [random.randint(0, 255) for _ in range(4)]
        
        dut.input_data_0.value = inputs[0]
        dut.input_data_1.value = inputs[1]
        dut.input_data_2.value = inputs[2]
        dut.input_data_3.value = inputs[3]
        
        dut.start.value = 1
        await RisingEdge(dut.clk)
        dut.start.value = 0
        
        while not dut.done.value:
            await RisingEdge(dut.clk)
        
        output_0 = dut.output_data_0.value
        output_1 = dut.output_data_1.value
        
        dut._log.info(f"Random test {i+1} - Inputs: {inputs}")
        dut._log.info(f"Random test {i+1} - Output 0: {output_0}, Output 1: {output_1}")
        
        # Basic sanity checks
        assert output_0 != 0, f"Output 0 should be non-zero for inputs {inputs}"
        assert output_1 != 0, f"Output 1 should be non-zero for inputs {inputs}"
        
        # Wait for done signal to be deasserted
        while dut.done.value:
            await RisingEdge(dut.clk)
