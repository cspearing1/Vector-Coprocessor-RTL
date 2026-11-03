import os
from cocotb_test.simulator import run

def test_vreg_runner():
    """Configures and runs the cocotb simulation using Icarus Verilog."""

    #Get the current working diectory path
    proj_path = os.path.dirname(os.path.abspath(__file__))

    #Run the cocotb simulation
    run(
        verilog_sources=[os.path.join(proj_path, "valu.sv")],
        toplevel="valu",
        module="test_valu",
        simulator="icarus",
        compile_args=["-g2012"],
    )