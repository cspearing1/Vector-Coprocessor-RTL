`timescale 1ns/1ps

module vreg #(
    parameter int ELEN     = 32,
    parameter int NUM_REGS = 8,
    parameter int ELENS    = 8,   // elements per register
    parameter int LANES    = 4
) (

    input logic clk,
    //Write port
    input logic [LANES*ELEN-1:0] wr_data, // input data for bank 0/1
    input logic wr_en, //write enable
    input logic [$clog2(NUM_REGS)-1:0] wr_addr, // which register to write to
    input logic wr_bank_sel, //which bank to write to

    //Read port A
    input logic rd_bank_sel, //which bank to read from
    input logic [$clog2(NUM_REGS)-1:0] rd_addr_a, //which register to read from port A
    output logic [LANES*ELEN-1:0] rd_data_a, //which data to read from port A

    //Read port B
    input logic [$clog2(NUM_REGS)-1:0] rd_addr_b, //which register to read from port B
    output logic [LANES*ELEN-1:0] rd_data_b  //which data to read from port B

);

//Storage Array: 2 Banks [0:1], 8 Registers [0:7], each ELEN*LANES bits wide
logic [LANES*ELEN-1:0] mem [0:1][0:NUM_REGS-1];

//Sequential Write Logic
always_ff @(posedge clk) begin
    if (wr_en) begin
        mem[wr_bank_sel][wr_addr] <= wr_data;
    end
end

//Combinational Read Logic
assign rd_data_a = mem[rd_bank_sel][rd_addr_a];
assign rd_data_b = mem[rd_bank_sel][rd_addr_b];

initial begin
    $dumpfile("vreg.vcd");
    $dumpvars(0, vreg);
end

endmodule
