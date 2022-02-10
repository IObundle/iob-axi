`timescale 1ns / 1ps

`include "axi.vh"

module iob2axi
  #(
    parameter ADDR_W = 0,
    parameter DATA_W = 0,
    // AXI-4 Full I/F parameters
    parameter AXI_ADDR_W = ADDR_W,
    parameter AXI_DATA_W = DATA_W
    )
   (
    input                  clk,
    input                  rst,

    //
    // Control I/F
    //
    input                  run,
    input                  direction, // 0 for reading, 1 for writing
    input [`AXI_LEN_W-1:0] length,
    output                 ready,
    output                 error,

    //
    // AXI-4 Full Master I/F
    //
    `AXI4_M_IF_PORT(m_),

    //
    // Native Slave I/F
    //
    input                  s_valid,
    input [ADDR_W-1:0]     s_addr,
    input [DATA_W-1:0]     s_wdata,
    input [DATA_W/8-1:0]   s_wstrb,
    output [DATA_W-1:0]    s_rdata,
    output                 s_ready
    );

   wire                    rd_run, wr_run;
   wire                    rd_ready, wr_ready;
   wire                    rd_error, wr_error;

   wire                    s_ready_rd, s_ready_wr;

   assign wr_run = direction? run: 1'b0;
   assign rd_run = direction? 1'b0: run;
   assign ready = wr_ready & rd_ready;
   assign error = rd_error | wr_error;

   assign s_ready = |s_wstrb? s_ready_wr: s_ready_rd;

   // AXI Read
   iob2axi_rd
     #(
       .ADDR_W(ADDR_W),
       .DATA_W(DATA_W)
       )
   iob2axi_rd0
     (
      .clk    (clk),
      .rst    (rst),

      // Control I/F
      .run    (rd_run),
      .length (length),
      .ready  (rd_ready),
      .error  (rd_error),

      // Native Slave I/F
      .s_valid (s_valid),
      .s_addr  (s_addr),
      .s_rdata (s_rdata),
      .s_ready (s_ready_rd),

      // AXI-4 full read master I/F
      `AXI4_READ_IF_PORTMAP(m_, m_)
      );

   // AXI Write
   iob2axi_wr
     # (
        .ADDR_W(ADDR_W),
        .DATA_W(DATA_W)
        )
   iob2axi_wr0
     (
      .clk     (clk),
      .rst     (rst),

      // Control I/F
      .run     (wr_run),
      .length  (length),
      .ready   (wr_ready),
      .error   (wr_error),

      // Native Slave I/F
      .s_valid (s_valid),
      .s_addr  (s_addr),
      .s_wdata (s_wdata),
      .s_wstrb (s_wstrb),
      .s_ready (s_ready_wr),

      // AXI-4 full write master I/F
      `AXI4_WRITE_IF_PORTMAP(m_, m_)
      );

endmodule
