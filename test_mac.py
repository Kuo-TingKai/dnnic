import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def mac_test_basic(dut):
    """Test basic MAC unit functionality: C = A * W + B"""

    # Test Case 1: Simple multiplication and accumulation (10 * 2 + 5)
    A_in_1 = 10
    W_in_1 = 2
    B_in_1 = 5
    expected_C_1 = 10 * 2 + 5  # 25

    dut.A.value = A_in_1
    dut.W.value = W_in_1
    dut.B.value = B_in_1

    await Timer(1, unit="ns")  # Wait for combinational logic to stabilize
    
    assert dut.C.value.integer == expected_C_1, \
        f"Test 1 failed: Expected {expected_C_1}, got {dut.C.value.integer}"
    dut._log.info(f"Test 1 passed: (10 * 2 + 5) = {dut.C.value.integer}")

@cocotb.test()
async def mac_test_max_values(dut):
    """Test MAC unit with maximum values (255 * 255 + 0)"""
    
    # Test Case 2: Maximum value multiplication (255 * 255 + 0)
    A_in_2 = 255
    W_in_2 = 255
    B_in_2 = 0
    expected_C_2 = 255 * 255 + 0  # 65025

    dut.A.value = A_in_2
    dut.W.value = W_in_2
    dut.B.value = B_in_2

    await Timer(1, unit="ns")
    
    assert dut.C.value.integer == expected_C_2, \
        f"Test 2 failed: Expected {expected_C_2}, got {dut.C.value.integer}"
    dut._log.info(f"Test 2 passed: (255 * 255 + 0) = {dut.C.value.integer}")

@cocotb.test()
async def mac_test_random(dut):
    """Test MAC unit with random values"""
    
    # Test Case 3: Random values test
    for i in range(10):
        A_in = random.randint(0, 255)
        W_in = random.randint(0, 255)
        B_in = random.randint(0, 32767)  # Limit to avoid overflow
        expected_C = A_in * W_in + B_in

        dut.A.value = A_in
        dut.W.value = W_in
        dut.B.value = B_in

        await Timer(1, unit="ns")
        
        assert dut.C.value.integer == expected_C, \
            f"Random test {i+1} failed: Expected {expected_C}, got {dut.C.value.integer}"
        dut._log.info(f"Random test {i+1} passed: ({A_in} * {W_in} + {B_in}) = {dut.C.value.integer}")

@cocotb.test()
async def mac_test_edge_cases(dut):
    """Test MAC unit with edge cases"""
    
    # Test Case 4: Zero multiplication (0 * anything + anything)
    dut.A.value = 0
    dut.W.value = 255
    dut.B.value = 100

    await Timer(1, unit="ns")
    
    assert dut.C.value.integer == 100, \
        f"Zero multiplication test failed: Expected 100, got {dut.C.value.integer}"
    dut._log.info(f"Zero multiplication test passed: (0 * 255 + 100) = {dut.C.value.integer}")
    
    # Test Case 5: Zero bias (anything * anything + 0)
    dut.A.value = 50
    dut.W.value = 3
    dut.B.value = 0

    await Timer(1, unit="ns")
    
    assert dut.C.value.integer == 150, \
        f"Zero bias test failed: Expected 150, got {dut.C.value.integer}"
    dut._log.info(f"Zero bias test passed: (50 * 3 + 0) = {dut.C.value.integer}")
