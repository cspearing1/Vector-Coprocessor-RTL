import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
import random

@cocotb.test()
async def test_valu(dut):
    """Randomised verification test for the vector ALU module."""

    dut.operand_a.value = 0
    dut.operand_b.value = 0
    dut.alu_op.value = 0
    await Timer(10, unit="ns")  # Wait 10ns for signals to stabilise

    dut._log.info("Starting ALU operation tests.")
    for i in range(10):  # Run 10 random tests
        alu_op = random.randint(0, 3)  # Randomly select an ALU operation (0 to 3)
        # Generate random 32-bit values for operand_a and operand_b
        operand_a = random.getrandbits(128)
        operand_b = random.getrandbits(128)
        dut.alu_op.value = alu_op
        dut.operand_a.value = operand_a
        dut.operand_b.value = operand_b
        await Timer(10, unit="ns")  # Wait 10ns for signals to stabilise

        res_lane = 0
        expected_result = 0
        for lane in range(4): # Loop through each lane (0 to 3) for 4 lanes

                a_lane = (operand_a >> (lane * 32)) & 0xFFFFFFFF  # Extract 32 bits for lane A
                b_lane = (operand_b >> (lane * 32)) & 0xFFFFFFFF  # Extract 32 bits for lane B

                if alu_op == 0:  # ADD
                    res_lane = (a_lane + b_lane) & 0xFFFFFFFF
                elif alu_op == 1:  # SUB
                    res_lane = (a_lane - b_lane) & 0xFFFFFFFF
                elif alu_op == 2:  # VMUL (LOW 32 BITS)
                    res_lane = (a_lane * b_lane) & 0xFFFFFFFF
                elif alu_op == 3:  # VMULH (HIGH 32 BITS)
                    # Convert to signed 32-bit integers for multiplication
                    a_signed = a_lane if a_lane < (1 << 31) else a_lane - (1 << 32)
                    b_signed = b_lane if b_lane < (1 << 31) else b_lane - (1 << 32)
                    full_product = a_signed * b_signed
                    res_lane = (full_product >> 32) & 0xFFFFFFFF

                expected_result |= res_lane << (lane * 32)  # Shift the result to the correct lane position

        #Read the result after all lanes complete
        read_value = int(dut.result.value)  # Read the result from the DUT

        assert read_value == expected_result, (f"Mismatch! Lane {lane}" 
                                                f"Expected {hex(expected_result)}, "
                                                f"got {hex(read_value)}\n" 
                                                f"Operand A: {hex(operand_a)}, "
                                                f"Operand B: {hex(operand_b)}, "
                                                f"ALU Op: {alu_op}")

    dut._log.info("All 50 randomised vector ALU tests passed.")