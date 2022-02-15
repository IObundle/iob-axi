`timescale 1ns / 1ps

`include "iob_lib.vh"
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
    input                clk,
    input                rst,

    //
    // Control I/F
    //
    input                run,
    input                direction, // 0 for reading, 1 for writing
    input [ADDR_W-1:0]   addr,
    output               ready,
    output               error,

    //
    // Native Slave I/F
    //
    input                s_valid,
    input [ADDR_W-1:0]   s_addr,
    input [DATA_W-1:0]   s_wdata,
    input [DATA_W/8-1:0] s_wstrb,
    output [DATA_W-1:0]  s_rdata,
    output               s_ready,

    //
    // AXI-4 Full Master I/F
    //
    `AXI4_M_IF_PORT(m_)
    );

   wire                  ready_rd, ready_wr;
   wire                  error_rd, error_wr;

   wire                  in_fifo_ready, out_fifo_ready;

   wire                  rd_valid, wr_valid;
   wire [ADDR_W-1:0]     rd_addr, wr_addr; //**
   wire [DATA_W-1:0]     wr_wdata;
   wire [DATA_W/8-1:0]   wr_wstrb;
   wire [DATA_W-1:0]     rd_rdata;
   wire                  rd_ready, wr_ready;

   assign ready = ready_wr & ready_rd;
   assign error = error_rd | error_wr;

   assign s_ready = |s_wstrb? in_fifo_ready: out_fifo_ready;

   //
   // Input FIFO
   //
   wire                       in_fifo_full;
   wire                       in_fifo_wr = s_valid & |s_wstrb & ~in_fifo_full;
   wire [DATA_W+DATA_W/8-1:0] in_fifo_wdata = {s_wdata, s_wstrb};

   wire                       in_fifo_empty;
   wire                       in_fifo_rd = wr_ready;
   wire [DATA_W+DATA_W/8-1:0] in_fifo_rdata;

   wire [`AXI_LEN_W:0]        in_fifo_level;

   assign wr_valid = ~in_fifo_empty;
   assign wr_wdata = in_fifo_rdata[DATA_W/8 +: DATA_W];
   assign wr_wstrb = in_fifo_rdata[0 +: DATA_W/8];

   assign in_fifo_ready = ~in_fifo_full;

   iob_fifo_sync
     #(
       .W_DATA_W(DATA_W+DATA_W/8),
       .R_DATA_W(DATA_W+DATA_W/8),
       .ADDR_W(`AXI_LEN_W)
       )
   iob_fifo_sync0
     (
      .clk     (clk),
      .rst     (rst),

      .w_en    (in_fifo_wr),
      .w_data  (in_fifo_wdata),
      .w_full  (in_fifo_full),

      .r_en    (in_fifo_rd),
      .r_data  (in_fifo_rdata),
      .r_empty (in_fifo_empty),

      .level   (in_fifo_level)
      );

   //
   // Output FIFO
   //
   wire                  out_fifo_full;
   wire                  out_fifo_wr = rd_ready;
   wire [DATA_W-1:0]     out_fifo_wdata = rd_rdata;

   wire                  out_fifo_empty;
   wire                  out_fifo_rd = s_valid & ~|s_wstrb & ~out_fifo_empty;
   wire [DATA_W-1:0]     out_fifo_rdata;

   wire [`AXI_LEN_W:0]   out_fifo_level;

   assign rd_valid = ~out_fifo_full;

   assign s_rdata = out_fifo_rdata;
   assign out_fifo_ready = ~out_fifo_empty;

   iob_fifo_sync
     #(
       .W_DATA_W(DATA_W),
       .R_DATA_W(DATA_W),
       .ADDR_W(`AXI_LEN_W)
       )
   iob_fifo_sync0
     (
      .clk     (clk),
      .rst     (rst),

      .w_en    (out_fifo_wr),
      .w_data  (out_fifo_wdata),
      .w_full  (out_fifo_full),

      .r_en    (out_fifo_rd),
      .r_data  (out_fifo_rdata),
      .r_empty (out_fifo_empty),

      .level   (out_fifo_level)
      );

   //
   // Compute next run
   //
   wire [`AXI_LEN_W:0]   length_int = direction? in_fifo_level: out_fifo_level;

   reg [`AXI_LEN_W-1:0]  count;
   wire                  count_en = ~&count & |length_int;

   wire                  run_int = ready & (length_int[`AXI_LEN_W] | &count);
   wire                  run_wr = direction? run_int: 1'b0;
   wire                  run_rd = direction? 1'b0: run_int;

   always @(posedge clk, posedge rst) begin
      if (rst) begin
         count <= `AXI_LEN_W'd0;
      end else if (run_int) begin
         count <= `AXI_LEN_W'd0;
      end else if (count_en) begin
         count <= count + 1'b1;
      end
   end

   //
   // Compute first address and burst length for the next data transfer
   //
   reg [`AXI_LEN_W-1:0]  length_burst;

   reg [ADDR_W-1:0]      addr_int, addr_int_next;
   wire [ADDR_W-1:0]     addr4k  = {addr_int[ADDR_W-1:12], {12{1'b1}}};
   wire [ADDR_W-1:0]     addrRem = addr_int + length_int - 1'b1;
   wire [ADDR_W-1:0]     minAddr = `min(addr4k, addrRem);

   always @(posedge clk, posedge rst) begin
      if (rst) begin
         addr_int <= {ADDR_W{1'b0}};
      end else if (run) begin
         addr_int <= addr;
      end else if (run_int) begin
         addr_int <= addr_int_next;
      end
   end

   always @* begin
      addr_int_next = minAddr + 1'b1;

      if (minAddr == addr4k) begin
         //addr_int_next = {{addr_int[ADDR_W-1:12] + 1'b1}, {12{1'b0}}};
         length_burst = addr_int - addr4k - 1'b1;
      end else begin // minAddr == addrRem
         //addr_int_next = addr_int + length_int;
         length_burst = length_int - 1'b1;
      end
   end

   //
   // AXI Read
   //
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
      .run    (run_rd),
      .addr   (addr_int),
      .length (length_burst),
      .ready  (ready_rd),
      .error  (error_rd),

      // Native Slave I/F
      .s_valid (rd_valid),
      .s_addr  (rd_addr),
      .s_rdata (rd_rdata),
      .s_ready (rd_ready),

      // AXI-4 full read master I/F
      `AXI4_READ_IF_PORTMAP(m_, m_)
      );

   //
   // AXI Write
   //
   iob2axi_wr
     #(
       .ADDR_W(ADDR_W),
       .DATA_W(DATA_W)
       )
   iob2axi_wr0
     (
      .clk     (clk),
      .rst     (rst),

      // Control I/F
      .run     (run_wr),
      .addr    (addr_int),
      .length  (length_burst),
      .ready   (ready_wr),
      .error   (error_wr),

      // Native Slave I/F
      .s_valid (wr_valid),
      .s_addr  (wr_addr),
      .s_wdata (wr_wdata),
      .s_wstrb (wr_wstrb),
      .s_ready (wr_ready),

      // AXI-4 full write master I/F
      `AXI4_WRITE_IF_PORTMAP(m_, m_)
      );

endmodule
