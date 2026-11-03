`timescale 1ns/1ps

module valu #(
    parameter int NUM_OPS = 4,
    parameter int LANES   = 4,
    parameter int ELEN    = 32
) (

    //Inputs
    input logic [LANES*ELEN-1:0] operand_a,
    input logic [LANES*ELEN-1:0] operand_b,
    input logic [$clog2(NUM_OPS)-1:0] alu_op,

    //Outputs
    output logic [LANES*ELEN-1:0] result,
    //#################################################
    // Individual lane outputs for easier debugging
    output logic [31:0] result_lane0, result_lane1, result_lane2, result_lane3
    //#################################################
);


assign result_lane0 = result[31:0];
assign result_lane1 = result[63:32];
assign result_lane2 = result[95:64];
assign result_lane3 = result[127:96];

genvar i;
generate
    for (i=0; i < LANES; i++) begin : g_lane
        logic [ELEN-1:0] a_lane, b_lane;
        logic signed [2*ELEN-1:0] full_product;

        assign a_lane = operand_a [i*ELEN +: ELEN];
        assign b_lane = operand_b [i*ELEN +: ELEN];
        assign full_product = $signed(a_lane) * $signed(b_lane);

        always_comb begin
            case (alu_op)
                2'b00: result [i*ELEN +: ELEN] = a_lane + b_lane; // Addition
                2'b01: result [i*ELEN +: ELEN] = a_lane - b_lane; // Subtraction
                2'b10: result [i*ELEN +: ELEN] = full_product[ELEN-1:0]; // Vector Multiply Low
                2'b11: result [i*ELEN +: ELEN] = full_product[2*ELEN-1:ELEN];//Vector Multiply High
                default: result[i*ELEN +: ELEN] = '0; // Default case
            endcase
        end
    end
endgenerate

// Waveform Dump for GTKWave
initial begin
    $dumpfile("valu.vcd");
    $dumpvars(0, valu);

end

endmodule
