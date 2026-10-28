# Vector Co-Processor

A vector co-processor for hardware acceleration, written in SystemVerilog and verified
with Cocotb (Python). 3rd-year individual project, University of Sheffield.

**Status:** In progress. Completed: vector register file. Next: vector ALU.

## Goals
A vector co-processor to accelerate operations common in machine learning, such as parallel vector arithmetic [e.g. element-wise add/multiply and multiply-accumulate]. Planned future work: integrating the accelerator with a RISC-V core.

## Design so far
- **Vector register file (`rtl/vreg.sv`):** [8 vector registers, each 256 bits (8 × 32-bit elements). Each register is stored as two 128-bit banks: bank 0 holds the lower 4 elements and bank 1 the upper 4. The datapath processes one 4-lane bank per pass. Two read ports, one write port; combinational reads, synchronous writes.]

## Verification
Testbenches in `tb/` use Cocotb with a Python runner.
- Basic read/write tests for the register file. [Tests: writing specified test data to chosen bank and register, data is then read from that register and compared to the expected value]

Run: `python tb/test_runner.py` (requires Python, Cocotb and [Icarus Verilog / Verilator]).

## Roadmap
- [ ] Vector ALU
- [ ] Control/decode
- [ ] Integration and FPGA testing

## Tools
SystemVerilog, Cocotb, GTKWave
