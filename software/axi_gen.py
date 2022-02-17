#!/usr/bin/python3

#
# axi_gen.py prefix typ
#
# typ = [master|slave]_[port|portmap|wire|tb]

import sys

#bus defaults
AXI_ADDR_W = 32
AXI_DATA_W = 32
AXIL_ADDR_W = 32
AXIL_DATA_W = 32
#bus constants
AXI_ID_W = 1
AXI_LEN_W = 8
AXI_SIZE_W = 3
AXI_BURST_W = 2
AXI_LOCK_W = 1
AXI_CACHE_W = 4
AXI_PROT_W = 3
AXI_QOS_W = 4
AXI_RESP_W = 2

def make_axi(AXI_ADDR_W, AXI_DATA_W):
    return [ \
['`OUTPUT(', AXI_ID_W,     'axi_awid',    'Address write channel ID'], \
['`OUTPUT(', AXI_ADDR_W,   'axi_awaddr',  'Address write channel address'], \
['`OUTPUT(', AXI_LEN_W,    'axi_awlen',   'Address write channel burst length'], \
['`OUTPUT(', AXI_SIZE_W,   'axi_awsize',  'Address write channel burst size. This signal indicates the size of each transfer in the burst'], \
['`OUTPUT(', AXI_BURST_W,  'axi_awburst', 'Address write channel burst type'], \
['`OUTPUT(', AXI_LOCK_W,   'axi_awlock',  'Address write channel lock type'], \
['`OUTPUT(', AXI_CACHE_W,  'axi_awcache', 'Address write channel memory type. Transactions set with Normal Non-cacheable Modifiable and Bufferable (0011).'], \
['`OUTPUT(', AXI_PROT_W,   'axi_awprot',  'Address write channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`OUTPUT(', AXI_QOS_W,    'axi_awqos',   'Address write channel quality of service'], \
['`OUTPUT(', 1,            'axi_awvalid', 'Address write channel valid'], \
['`INPUT(', 1,             'axi_awready', 'Address write channel ready'], \
['`OUTPUT(', AXI_ID_W,     'axi_wid',     'Write channel ID'], \
['`OUTPUT(', AXI_DATA_W,   'axi_wdata',   'Write channel data'], \
['`OUTPUT(', AXI_DATA_W/8, 'axi_wstrb',   'Write channel write strobe'], \
['`OUTPUT(', 1,            'axi_wlast',   'Write channel last word flag'], \
['`OUTPUT(', 1,            'axi_wvalid',  'Write channel valid'], \
['`INPUT(',  1,            'axi_wready',  'Write channel ready'], \
['`INPUT(', AXI_ID_W,      'axi_bid',     'Write response channel ID'], \
['`INPUT(', AXI_RESP_W,    'axi_bresp',   'Write response channel response'], \
['`INPUT(', 1,             'axi_bvalid',  'Write response channel valid'], \
['`OUTPUT(', 1,            'axi_bready',  'Write response channel ready'], \
['`OUTPUT(', AXI_ID_W,     'axi_arid',    'Address read channel ID'], \
['`OUTPUT(', AXI_ADDR_W,   'axi_araddr',  'Address read channel address'], \
['`OUTPUT(', AXI_LEN_W,    'axi_arlen',   'Address read channel burst length'], \
['`OUTPUT(', AXI_SIZE_W,   'axi_arsize',  'Address read channel burst size. This signal indicates the size of each transfer in the burst'], \
['`OUTPUT(', AXI_BURST_W,  'axi_arburst', 'Address read channel burst type'], \
['`OUTPUT(', AXI_LOCK_W,   'axi_arlock',  'Address read channel lock type'], \
['`OUTPUT(', AXI_CACHE_W,  'axi_arcache', 'Address read channel memory type. Transactions set with Normal Non-cacheable Modifiable and Bufferable (0011).'], \
['`OUTPUT(', AXI_PROT_W,   'axi_arprot',  'Address read channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`OUTPUT(', AXI_QOS_W,    'axi_arqos',   'Address read channel quality of service'], \
['`OUTPUT(', 1,            'axi_arvalid', 'Address read channel valid'], \
['`INPUT(', 1,             'axi_arready', 'Address read channel ready'], \
['`INPUT(', AXI_ID_W,      'axi_rid',     'Read channel ID'], \
['`INPUT(', AXI_DATA_W,    'axi_rdata',   'Read channel data'], \
['`INPUT(', AXI_RESP_W,    'axi_rresp',   'Read channel response'], \
['`INPUT(', 1,             'axi_rlast',   'Read channel last word'], \
['`INPUT(', 1,             'axi_rvalid',  'Read channel valid' ], \
['`OUTPUT(', 1,            'axi_rready' , 'Read channel ready'] \
]

def make_axil(AXIL_ADDR_W, AXIL_DATA_W):
    return [ \
['`OUTPUT(', AXI_ID_W,     'axil_awid',    'Address write channel ID'], \
['`OUTPUT(', AXIL_ADDR_W,   'axil_awaddr',  'Address write channel address'], \
['`OUTPUT(', AXI_PROT_W,   'axil_awprot',  'Address write channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`OUTPUT(', AXI_QOS_W,    'axil_awqos',   'Address write channel quality of service'], \
['`OUTPUT(', 1,            'axil_awvalid', 'Address write channel valid'], \
['`INPUT(', 1,             'axil_awready', 'Address write channel ready'], \
['`OUTPUT(', AXI_ID_W,     'axil_wid',     'Write channel ID'], \
['`OUTPUT(', AXIL_DATA_W,   'axil_wdata',   'Write channel data'], \
['`OUTPUT(', AXIL_DATA_W/8, 'axil_wstrb',   'Write channel write strobe'], \
['`OUTPUT(', 1,            'axil_wvalid',  'Write channel valid'], \
['`INPUT(',  1,            'axil_wready',  'Write channel ready'], \
['`INPUT(', AXI_ID_W,      'axil_bid',     'Write response channel ID'], \
['`INPUT(', AXI_RESP_W,    'axil_bresp',   'Write response channel response'], \
['`INPUT(', 1,             'axil_bvalid',  'Write response channel valid'], \
['`OUTPUT(', 1,            'axil_bready',  'Write response channel ready'], \
['`OUTPUT(', AXI_ID_W,     'axil_arid',    'Address read channel ID'], \
['`OUTPUT(', AXIL_ADDR_W,   'axil_araddr',  'Address read channel address'], \
['`OUTPUT(', AXI_PROT_W,   'axil_arprot',  'Address read channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`OUTPUT(', AXI_QOS_W,    'axil_arqos',   'Address read channel quality of service'], \
['`OUTPUT(', 1,            'axil_arvalid', 'Address read channel valid'], \
['`INPUT(', 1,             'axil_arready', 'Address read channel ready'], \
['`INPUT(', AXI_ID_W,      'axil_rid',     'Read channel ID'], \
['`INPUT(', AXIL_DATA_W,    'axil_rdata',   'Read channel data'], \
['`INPUT(', AXI_RESP_W,    'axil_rresp',   'Read channel response'], \
['`INPUT(', 1,             'axil_rvalid',  'Read channel valid' ], \
['`OUTPUT(', 1,            'axil_rready' , 'Read channel ready'] \
]


def reverse(direction):
    if direction == '`INPUT(':
        return '`OUTPUT('
    elif direction == '`OUTPUT(':
        return '`INPUT('
    else:
        print("ERROR: reverse_direction : invalid argument")
        quit()
        
def tbsignal(direction):
    if direction == '`INPUT(':
        return '`WIRE('
    elif direction == '`OUTPUT(':
        return '`VAR('
    else:
        print("ERROR: tb_reciprocal : invalid argument")
        quit()

#AXI FULL
        
def axi_m_port():
    for i in range(len(axi_m)):
        fout.write(axi_m[i][0]+axi_m[i][2]+', '+str(int(axi_m[i][1]))+'), //'+axi_m[i][3]+'\n')
    
def axi_s_port():
    for i in range(len(axi_m)):
        fout.write(reverse(axi_m[i][0])+axi_m[i][2]+', '+str(int(axi_m[i][1]))+'), //'+axi_m[i][3]+'\n')


def axi_portmap(prefix):
    for i in range(len(axi_m)):
        fout.write('.'+axi_m[i][2]+'('+prefix+axi_m[i][2]+'), //'+axi_m[i][3]+'\n')

def axi_m_tb(prefix):
    for i in range(len(axi_m)):
        fout.write(tbsignal(axi_m[i][0])+prefix+axi_m[i][2]+', '+str(int(axi_m[i][1]))+') //'+axi_m[i][3]+'\n')
    
def axi_s_tb(prefix):
    for i in range(len(axi_m)):
        fout.write(tbsignal(reverse(axi_m[i][0]))+prefix+axi_m[i][2]+', '+str(int(axi_m[i][1]))+') //'+axi_m[i][3]+'\n')

def axi_wire(prefix):
    for i in range(len(axi_m)):
        fout.write('`WIRE('+prefix+axi_m[i][2]+', '+str(int(axi_m[i][1]))+') //'+axi_m[i][3]+'\n')
        

#AXI LITE

def axil_m_port():
    for i in range(len(axil_m)):
        fout.write(axil_m[i][0]+axil_m[i][2]+', '+str(int(axil_m[i][1]))+'), //'+axil_m[i][3]+'\n')
    
def axil_s_port():
    for i in range(len(axil_m)):
        fout.write(reverse(axil_m[i][0])+axil_m[i][2]+', '+str(int(axil_m[i][1]))+'), //'+axil_m[i][3]+'\n')


def axil_portmap(prefix):
    for i in range(len(axil_m)):
        fout.write('.'+axil_m[i][2]+'('+prefix+axil_m[i][2]+'), //'+axil_m[i][3]+'\n')

def axil_m_tb(prefix):
    for i in range(len(axil_m)):
        fout.write(tbsignal(axil_m[i][0])+prefix+axil_m[i][2]+', '+str(int(axil_m[i][1]))+') //'+axil_m[i][3]+'\n')
    
def axil_s_tb(prefix):
    for i in range(len(axil_m)):
        fout.write(tbsignal(reverse(axil_m[i][0]))+prefix+axil_m[i][2]+', '+str(int(axil_m[i][1]))+') //'+axil_m[i][3]+'\n')

def axil_wire(prefix):
    for i in range(len(axil_m)):
        fout.write('`WIRE('+prefix+axil_m[i][2]+', '+str(int(axil_m[i][1]))+') //'+axil_m[i][3]+'\n')

        
#parse command line arguments
if len(sys.argv) < 3 or len(sys.argv) > 5:
    print(len(sys.argv))
    print("Usage:  axi_gen.py prefix typ aw dw")
    quit()
if len(sys.argv) > 3:
    AXI_ADDR_W = int(sys.argv[3])
    AXIL_ADDR_W = int(sys.argv[3])
if len(sys.argv) > 4:
    AXI_DATA_W = int(sys.argv[4])
    AXIL_DATA_W = int(sys.argv[4])

prefix = sys.argv[1]
typ = sys.argv[2]

#make master buses
global axi_m
axi_m = make_axi(AXI_ADDR_W, AXI_DATA_W)
global axil_m
axil_m = make_axil(AXIL_ADDR_W, AXIL_DATA_W)

#open output .vh file
fout = open (prefix+typ+".vh", 'w')


#call function to generate .vh file
if typ.find("m_port")>=0 or typ.find("s_port")>=0:
    eval(typ+'()')
else:
    eval(typ+"('"+prefix+"')")


