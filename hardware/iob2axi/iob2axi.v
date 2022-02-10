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
    input                  clk,
    input                  rst,

    //
    // Control I/F
    //
    /*input                  run,
    input                  direction, // 0 for reading, 1 for writing*/
    input [AXI_ADDR_W-1:0] addr,
    input [`AXI_LEN_W-1:0] length,
    output                 ready,
    output                 error,

    //
    // Native Slave I/F
    //
    input                  s_valid,
    input [ADDR_W-1:0]     s_addr,
    input [DATA_W-1:0]     s_wdata,
    input [DATA_W/8-1:0]   s_wstrb,
    output [DATA_W-1:0]    s_rdata,
    output                 s_ready,

    //
    // AXI-4 Full Master I/F
    //
    `AXI4_M_IF_PORT(m_)
    );

   wire                    run_rd, run_wr;
   wire                    ready_rd, ready_wr;
   wire                    error_rd, error_wr;

   wire                    rd_ready, wr_ready;
   reg                     fifo_ready;

   /*assign run_wr = direction? run: 1'b0;
   assign run_rd = direction? 1'b0: run;*/
   assign ready = ready_wr & ready_rd;
   assign error = error_rd | error_wr;

   assign s_rdata = rd_data;
   assign s_ready = |s_wstrb? fifo_ready: rd_ready;

   //
   // Input FIFO
   //
   wire                       w_full;
   wire                       w_en = s_valid & |s_wstrb & ~w_full;
   wire [DATA_W+DATA_W/8-1:0] w_data = {s_wdata, s_wstrb};

   wire                       r_empty;
   wire                       r_en = wr_valid & |wr_wstrb;
   wire [DATA_W+DATA_W/8-1:0] r_data;

   wire [ADDR_W:0]            level;

   assign wr_wdata = r_data[DATA_W/8 +: DATA_W];
   assign wr_wstrb = r_data[0 +: DATA_W/8];

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

      .w_en    (w_en),
      .w_data  (w_data),
      .w_full  (w_full),

      .r_en    (r_en),
      .r_data  (r_data),
      .r_empty (r_empty),

      .level   (level)
      );

   always @(posedge clk, posedge rst) begin
      if (rst) begin
         fifo_ready <= 1'b0;
      end else if (~w_full) begin
         fifo_ready <= s_valid;
      end else begin
         fifo_ready <= 1'b0;
      end
   end

   //
   // Compute first address and burst length for the next data transfer
   //
   wire [AXI_ADDR_W-1:0]   addr4k  = {addr_int[AXI_ADDR_W-1:12], {12{1'b1}}};
   wire [AXI_ADDR_W-1:0]   addrRem = addr_int + length_int;
   wire [AXI_ADDR_W-1:0]   minAddr = `min(addr4k, addrRem);

   reg [`AXI_LEN_W-1:0]    length_int;
   reg [`AXI_LEN_W-1:0]    length_burst;

   always @(posedge clk, posedge rst) begin
      if (rst) begin
         addr_int <= `AXI_LEN_W'd0;
      end else if (run) begin
         addr_int <= addr;
      end else if () begin
         addr_int <= addr_int_next;
      end
   end

   always @(posedge clk, posedge rst) begin
      if (rst) begin
         length_burst <= `AXI_LEN_W'd0;
      end else begin
         length_burst <= length_burst_next;
      end
   end

   always @* begin
      if (minAddr == addr4k) begin
         addr_int_next = {{addr_int[AXI_ADDR_W-1:12] + 1'b1}, {12{1'b0}}};
         length_burst_next = addr_int - addr4k - 1'b1;
      end else begin // minAddr == addrRem
         addr_int_next = addr_int + length_in;
         length_burst_next = length_int - 1'b1;  // - 1'b1???
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
