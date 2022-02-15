`timescale 1ns / 1ps

`include "axi.vh"

module iob2axil #
  (
   parameter AXIL_ADDR_W = 32, // Width of address bus in bits
   parameter AXIL_DATA_W = 32  // Width of data bus in bits
   )
   (
    input                        clk,
    input                        rst,

    //
    // AXI-4 lite master interface
    //
    `AXI4_LITE_M_IF_PORT(m_),

    //
    // Native slave interface
    //
    input                        valid,
    input [AXIL_ADDR_W-1:0]      addr,
    input [AXIL_DATA_W-1:0]      wdata,
    input [AXIL_DATA_W/8-1:0]    wstrb,
    output reg [AXIL_DATA_W-1:0] rdata,
    output                       ready
    );

   assign m_axil_awaddr  = addr;
   assign m_axil_araddr  = addr;
   assign m_axil_wdata   = wdata;
   assign m_axil_wstrb   = wstrb;

   // AXI IDs
   assign m_axil_awid = `AXI_ID_W'd0;
   assign m_axil_wid  = `AXI_ID_W'd0;
   assign m_axil_arid = `AXI_ID_W'd0;

   // Protection types
   assign m_axil_awprot = `AXI_PROT_W'd2;
   assign m_axil_arprot = `AXI_PROT_W'd2;

   // Quality of services
   assign m_axil_awqos = `AXI_QOS_W'd0;
   assign m_axil_arqos = `AXI_QOS_W'd0;

   always @(posedge clk, posedge rst) begin
      if (rst) begin
         rdata <= {AXIL_DATA_W{1'b0}};
      end else begin
         rdata <= m_axil_rdata;
      end
   end

   wire                          wr = valid & |wstrb;
   wire                          rd = valid & ~|wstrb;
   reg                           wr_reg, rd_reg;
   always @(posedge clk, posedge rst) begin
      if (rst) begin
         wr_reg <= 1'b0;
         rd_reg <= 1'b0;
      end else begin
         wr_reg <= wr;
         rd_reg <= rd;
      end
   end

   reg                           awvalid_ack;
   assign m_axil_awvalid = (wr | wr_reg) & ~awvalid_ack;
   always @(posedge clk, posedge rst) begin
      if (rst) begin
         awvalid_ack <= 1'b0;
      end else if (m_axil_awvalid & m_axil_awready) begin
         awvalid_ack <= 1'b1;
      end else if (m_axil_bvalid) begin
         awvalid_ack <= 1'b0;
      end
   end

   reg                           wvalid_ack;
   assign m_axil_wvalid = (wr | wr_reg)  & ~wvalid_ack;
   always @(posedge clk, posedge rst) begin
      if (rst) begin
         wvalid_ack <= 1'b0;
      end else if (m_axil_wvalid & m_axil_wready) begin
         wvalid_ack <= 1'b1;
      end else begin
         wvalid_ack <= 1'b0;
      end
   end

   assign m_axil_bready = 1'b1;

   reg                           arvalid_ack;
   assign m_axil_arvalid = (rd | rd_reg) & ~arvalid_ack;
   always @(posedge clk, posedge rst) begin
      if (rst) begin
         arvalid_ack <= 1'b0;
      end else if (m_axil_arvalid & m_axil_arready) begin
         arvalid_ack <= 1'b1;
      end else if (m_axil_rvalid) begin
         arvalid_ack <= 1'b0;
      end
   end

   reg                           rready_ack;
   assign m_axil_rready = (rd | rd_reg) & ~rready_ack;
   always @(posedge clk, posedge rst) begin
      if (rst) begin
         rready_ack <= 1'b0;
      end else if (m_axil_rvalid & m_axil_rready) begin
         rready_ack <= 1'b1;
      end else begin
         rready_ack <= 1'b0;
      end
   end

   assign ready = m_axil_bvalid | rready_ack;

endmodule
