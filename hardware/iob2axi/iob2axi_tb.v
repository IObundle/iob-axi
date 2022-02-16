`timescale 1ns / 1ps

`include "axi.vh"

`define CLK_PER 10

module iob2axi_tb;

   parameter TEST_SZ = 1024;

   parameter ADDR_W = 24;
   parameter DATA_W = 32;

   parameter AXI_ADDR_W = ADDR_W;
   parameter AXI_DATA_W = DATA_W;

   // Clock
   reg clk = 1;
   always #(`CLK_PER/2) clk = ~clk;

   // Reset
   reg rst = 0;

   //
   // DMA interface
   //

   // Control I/F
   reg run;
   reg direction;
   reg [ADDR_W-1:0] start_addr;
   wire             ready;
   wire             error;

   // Native slave I/F
   reg              s_valid;
   reg [ADDR_W-1:0] s_addr;
   reg [DATA_W-1:0] s_wdata;
   reg [DATA_W/8-1:0] s_wstrb;
   wire [DATA_W-1:0]  s_rdata;
   wire               s_ready;

   // AXI-4 full master I/F
   `AXI4_IF_WIRE(ddr_);

   // Iterators
   integer            i, seq_ini;

   initial begin

`ifdef VCD
      $dumpfile("uut.vcd");
      $dumpvars();
`endif

      //
      // Init signals
      //
      run = 0;
      start_addr = 0;
      direction = 0;

      s_valid = 0;
      s_addr = 0;
      s_wdata = 0;
      s_wstrb = 0;

      //
      // Initialize memory
      //

      // Assert reset
      #100 rst = 1;

      // Deassert rst
      repeat (10) @(posedge clk) #1;
      rst = 0;

      // Wait an arbitray (10) number of cycles
      repeat (10) @(posedge clk) #1;

      //
      // Test starts here
      //

      // Write test

      direction = 1;
      start_addr = 'h8000 - 'd10 -'d1;

      run = 1;
      @(posedge clk) #1;
      run = 0;

      s_valid = 1;
      s_wstrb = 4'hf;

      // Number from which to start the incremental sequence to initialize the RAM
      seq_ini = 32;
      for (i=0; i < TEST_SZ; i=i+1) begin
         s_addr = i;
         s_wdata = i+seq_ini;
         do
            @(posedge clk) #1;
         while(~s_ready);
      end
      s_valid = 0;

      repeat(4) @(posedge clk) #1;

      // Read test

      direction = 0;

      s_valid = 1;
      s_wstrb = 4'h0;

      for (i=0; i < TEST_SZ; i=i+1) begin
         s_addr = i;
         do
            @(posedge clk) #1;
         while(~s_ready);

         if (s_rdata != i+seq_ini) begin
            $display("ERROR: Test failed! At position %d, data=%h and s_rdata=%h.", i, i+seq_ini, s_rdata);
         end
      end
      s_valid = 0;

      $display("INFO: Test completed successfully!");

      repeat(10) @(posedge clk) #1;

      $finish;
   end

   iob2axi
     #(
       .ADDR_W(ADDR_W),
       .DATA_W(DATA_W)
       )
   uut
     (
      .clk       (clk),
      .rst       (rst),

      //
      // Control I/F
      //
      .run       (run),
      .direction (direction),
      .addr      (start_addr),
      .ready     (ready),
      .error     (error),

      //
      // Native slave I/F
      //
      .s_valid (s_valid),
      .s_addr  (s_addr),
      .s_wdata (s_wdata),
      .s_wstrb (s_wstrb),
      .s_rdata (s_rdata),
      .s_ready (s_ready),

      //
      // AXI-4 full master I/F
      //
      `AXI4_IF_PORTMAP(m_, ddr_)
      );

   axi_ram
     #(
       .ID_WIDTH   (`AXI_ID_W),
       .DATA_WIDTH (AXI_DATA_W),
       .ADDR_WIDTH (AXI_ADDR_W)
       )
   axi_ram0
     (
      .clk            (clk),
      .rst            (rst),

      //
      // AXI-4 full master interface
      //

      // Address write
      .s_axi_awid     (ddr_axi_awid),
      .s_axi_awaddr   (ddr_axi_awaddr),
      .s_axi_awlen    (ddr_axi_awlen),
      .s_axi_awsize   (ddr_axi_awsize),
      .s_axi_awburst  (ddr_axi_awburst),
      .s_axi_awlock   (ddr_axi_awlock),
      .s_axi_awprot   (ddr_axi_awprot),
      .s_axi_awcache  (ddr_axi_awcache),
      .s_axi_awvalid  (ddr_axi_awvalid),
      .s_axi_awready  (ddr_axi_awready),

      // Write
      .s_axi_wvalid   (ddr_axi_wvalid),
      .s_axi_wdata    (ddr_axi_wdata),
      .s_axi_wstrb    (ddr_axi_wstrb),
      .s_axi_wlast    (ddr_axi_wlast),
      .s_axi_wready   (ddr_axi_wready),

      // Write response
      .s_axi_bid      (ddr_axi_bid),
      .s_axi_bvalid   (ddr_axi_bvalid),
      .s_axi_bresp    (ddr_axi_bresp),
      .s_axi_bready   (ddr_axi_bready),

      // Address read
      .s_axi_arid     (ddr_axi_arid),
      .s_axi_araddr   (ddr_axi_araddr),
      .s_axi_arlen    (ddr_axi_arlen),
      .s_axi_arsize   (ddr_axi_arsize),
      .s_axi_arburst  (ddr_axi_arburst),
      .s_axi_arlock   (ddr_axi_arlock),
      .s_axi_arcache  (ddr_axi_arcache),
      .s_axi_arprot   (ddr_axi_arprot),
      .s_axi_arvalid  (ddr_axi_arvalid),
      .s_axi_arready  (ddr_axi_arready),

      // Read
      .s_axi_rid      (ddr_axi_rid),
      .s_axi_rvalid   (ddr_axi_rvalid),
      .s_axi_rdata    (ddr_axi_rdata),
      .s_axi_rlast    (ddr_axi_rlast),
      .s_axi_rresp    (ddr_axi_rresp),
      .s_axi_rready   (ddr_axi_rready)
      );

endmodule
