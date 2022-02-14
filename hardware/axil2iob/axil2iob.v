`timescale 1ns / 1ps

`include "axi.vh"

module axil2iob #
  (
   parameter AXIL_ADDR_W = 32, // Width of address bus in bits
   parameter AXIL_DATA_W = 32  // Width of data bus in bits
   )
   (
    input                      clk,
    input                      rst,

    //
    // AXI-4 lite slave interface
    //
    `AXI4_LITE_S_IF_PORT(s_),

    //
    // Native master interface
    //
    output                     valid,
    output [AXIL_ADDR_W-1:0]   addr,
    output [AXIL_DATA_W-1:0]   wdata,
    output [AXIL_DATA_W/8-1:0] wstrb,
    input [AXIL_DATA_W-1:0]    rdata,
    input                      ready
    );

   reg                         awvalid_ack;
   reg                         arvalid_ack;

   assign s_axil_rdata = rdata;

   // AXI IDs
   assign s_axil_bid = `AXI_ID_W'd0;
   assign s_axil_rid = `AXI_ID_W'd0;

   // Response is always OK
   assign s_axil_bresp = `AXI_RESP_W'd0;
   assign s_axil_rresp = `AXI_RESP_W'd0;

   assign valid = (s_axil_wvalid | s_axil_arvalid) & ~ready;
   assign addr  = s_axil_wvalid? s_axil_awaddr: s_axil_araddr;
   assign wstrb = s_axil_wvalid? s_axil_wstrb: {(AXIL_DATA_W/8){1'b0}};
   assign wdata = s_axil_wdata;

   assign s_axil_awready = awvalid_ack & ready;
   assign s_axil_wready  = awvalid_ack & ready;
   assign s_axil_arready = arvalid_ack & ready;
   assign s_axil_rvalid  = arvalid_ack & ready;

   reg                         s_axil_bvalid_int;
   assign s_axil_bvalid = s_axil_bvalid_int;
   always @(posedge clk, posedge rst) begin
      if (rst) begin
         s_axil_bvalid_int <= 1'b0;
      end else begin
         s_axil_bvalid_int <= s_axil_wready;
      end
   end

   always @(posedge clk, posedge rst) begin
      if (rst) begin
         awvalid_ack <= 1'b0;
      end else if (s_axil_awvalid) begin
         awvalid_ack <= 1'b1;
      end else if (ready) begin
         awvalid_ack <= 1'b0;
      end
   end

   always @(posedge clk, posedge rst) begin
      if (rst) begin
         arvalid_ack <= 1'b0;
      end else if (s_axil_arvalid) begin
         arvalid_ack <= 1'b1;
      end else if (ready) begin
         arvalid_ack <= 1'b0;
      end
   end

endmodule
