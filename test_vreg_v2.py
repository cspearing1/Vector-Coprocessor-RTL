import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
import random

@cocotb.test()
async def test_vreg_basic(dut):

    # Create a 10ns period clock (100MHz) on port 'clk'
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    NUM_REGS = 8  # Number of registers in the vector register file
    NUM_BANKS = 2  # Number of banks in the vector register file

    expected_mem = {} # Dictionary to hold expected values for each bank and register

    dut.wr_en.value = 0
    dut.wr_data.value = 0
    dut.wr_addr.value = 0
    dut.wr_bank_sel.value = 0

    dut.rd_bank_sel.value = 0
    dut.rd_addr_a.value = 0
    dut.rd_addr_b.value = 0

    await RisingEdge(dut.clk)  # Wait for the next rising edge of the clock

    #Write unique random values to each register in both banks
    dut.wr_en.value = 1
    dut._log.info("Starting write operations to all registers in both banks.")

    for bank in range(NUM_BANKS):
        for reg in range(NUM_REGS):
            test_pattern = random.randint(0, (1 << 128) - 1)  # Unique pattern for each register
            expected_mem[(bank, reg)] = test_pattern  # Store the expected value

            dut.wr_data.value = test_pattern
            dut.wr_addr.value = reg
            dut.wr_bank_sel.value = bank
            await RisingEdge(dut.clk)  # Wait for the next rising edge of the clock

    dut.wr_en.value = 0  # Disable write after all writes are done
    await Timer(1, unit="ns")  # Wait for a short time for combinational propagation

    #Read back and verify the values from each register in both banks
    dut._log.info("Starting read operations to verify all registers in both banks.")
    for bank in range(NUM_BANKS):
        for reg in range(NUM_REGS):
            # Read port A gets current register, port B gets the next register (wrapping around)
            reg_a = reg
            reg_b = (reg + 1) % NUM_REGS 

            dut.rd_bank_sel.value = bank
            dut.rd_addr_a.value = reg_a
            dut.rd_addr_b.value = reg_b
            await Timer(1, unit="ns")  # Wait for a short time for combinational propagation

            # Read values from both ports
            read_value_a = int(dut.rd_data_a.value)
            read_value_b = int(dut.rd_data_b.value)

            expected_a = expected_mem[(bank, reg_a)]
            expected_b = expected_mem[(bank, reg_b)]

            assert read_value_a == expected_a, f"Mismatch! Bank {bank}, Register {reg_a}: Expected {hex(expected_a)}, got {hex(read_value_a)}"
            assert read_value_b == expected_b, f"Mismatch! Bank {bank}, Register {reg_b}: Expected {hex(expected_b)}, got {hex(read_value_b)}"

    dut._log.info("All read values matched the expected values. Test passed.")