#!/usr/bin/python3

#
# type = [master|slave]_[port|portmap|wire|tb] or [master|slave]_[write|read]_[port|portmap|wire|tb]
#

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

axi_m = []

#
# AXI-4 Full
#

def make_axi_write(AXI_ADDR_W, AXI_DATA_W):
    return [ \
['`IOB_OUTPUT(', AXI_ID_W,        'axi_awid',    'Address write channel ID'], \
['`IOB_OUTPUT(', AXI_ADDR_W,      'axi_awaddr',  'Address write channel address'], \
['`IOB_OUTPUT(', AXI_LEN_W,       'axi_awlen',   'Address write channel burst length'], \
['`IOB_OUTPUT(', AXI_SIZE_W,      'axi_awsize',  'Address write channel burst size. This signal indicates the size of each transfer in the burst'], \
['`IOB_OUTPUT(', AXI_BURST_W,     'axi_awburst', 'Address write channel burst type'], \
['`IOB_OUTPUT(', AXI_LOCK_W,      'axi_awlock',  'Address write channel lock type'], \
['`IOB_OUTPUT(', AXI_CACHE_W,     'axi_awcache', 'Address write channel memory type. Transactions set with Normal Non-cacheable Modifiable and Bufferable (0011).'], \
['`IOB_OUTPUT(', AXI_PROT_W,      'axi_awprot',  'Address write channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`IOB_OUTPUT(', AXI_QOS_W,       'axi_awqos',   'Address write channel quality of service'], \
['`IOB_OUTPUT(', 1,               'axi_awvalid', 'Address write channel valid'], \
['`IOB_INPUT(',  1,               'axi_awready', 'Address write channel ready'], \
['`IOB_OUTPUT(', AXI_ID_W,        'axi_wid',     'Write channel ID'], \
['`IOB_OUTPUT(', AXI_DATA_W,      'axi_wdata',   'Write channel data'], \
['`IOB_OUTPUT(', AXI_DATA_W+'/8', 'axi_wstrb',   'Write channel write strobe'], \
['`IOB_OUTPUT(', 1,               'axi_wlast',   'Write channel last word flag'], \
['`IOB_OUTPUT(', 1,               'axi_wvalid',  'Write channel valid'], \
['`IOB_INPUT(',  1,               'axi_wready',  'Write channel ready'], \
['`IOB_INPUT(',  AXI_ID_W,        'axi_bid',     'Write response channel ID'], \
['`IOB_INPUT(',  AXI_RESP_W,      'axi_bresp',   'Write response channel response'], \
['`IOB_INPUT(',  1,               'axi_bvalid',  'Write response channel valid'], \
['`IOB_OUTPUT(', 1,               'axi_bready',  'Write response channel ready'] \
]

def make_axi_read(AXI_ADDR_W, AXI_DATA_W):
    return [ \
['`IOB_OUTPUT(', AXI_ID_W,        'axi_arid',    'Address read channel ID'], \
['`IOB_OUTPUT(', AXI_ADDR_W,      'axi_araddr',  'Address read channel address'], \
['`IOB_OUTPUT(', AXI_LEN_W,       'axi_arlen',   'Address read channel burst length'], \
['`IOB_OUTPUT(', AXI_SIZE_W,      'axi_arsize',  'Address read channel burst size. This signal indicates the size of each transfer in the burst'], \
['`IOB_OUTPUT(', AXI_BURST_W,     'axi_arburst', 'Address read channel burst type'], \
['`IOB_OUTPUT(', AXI_LOCK_W,      'axi_arlock',  'Address read channel lock type'], \
['`IOB_OUTPUT(', AXI_CACHE_W,     'axi_arcache', 'Address read channel memory type. Transactions set with Normal Non-cacheable Modifiable and Bufferable (0011).'], \
['`IOB_OUTPUT(', AXI_PROT_W,      'axi_arprot',  'Address read channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`IOB_OUTPUT(', AXI_QOS_W,       'axi_arqos',   'Address read channel quality of service'], \
['`IOB_OUTPUT(', 1,               'axi_arvalid', 'Address read channel valid'], \
['`IOB_INPUT(',  1,               'axi_arready', 'Address read channel ready'], \
['`IOB_INPUT(',  AXI_ID_W,        'axi_rid',     'Read channel ID'], \
['`IOB_INPUT(',  AXI_DATA_W,      'axi_rdata',   'Read channel data'], \
['`IOB_INPUT(',  AXI_RESP_W,      'axi_rresp',   'Read channel response'], \
['`IOB_INPUT(',  1,               'axi_rlast',   'Read channel last word'], \
['`IOB_INPUT(',  1,               'axi_rvalid',  'Read channel valid' ], \
['`IOB_OUTPUT(', 1,               'axi_rready' , 'Read channel ready'] \
]

def make_axi(AXI_ADDR_W, AXI_DATA_W):
    return make_axi_write(AXI_ADDR_W, AXI_DATA_W) + make_axi_read(AXI_ADDR_W, AXI_DATA_W)

#
# AXI-4 Lite
#

def make_axil_write(AXIL_ADDR_W, AXIL_DATA_W):
    return [ \
['`IOB_OUTPUT(', AXI_ID_W,         'axil_awid',    'Address write channel ID'], \
['`IOB_OUTPUT(', AXIL_ADDR_W,      'axil_awaddr',  'Address write channel address'], \
['`IOB_OUTPUT(', AXI_PROT_W,       'axil_awprot',  'Address write channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`IOB_OUTPUT(', AXI_QOS_W,        'axil_awqos',   'Address write channel quality of service'], \
['`IOB_OUTPUT(', 1,                'axil_awvalid', 'Address write channel valid'], \
['`IOB_INPUT(',  1,                'axil_awready', 'Address write channel ready'], \
['`IOB_OUTPUT(', AXI_ID_W,         'axil_wid',     'Write channel ID'], \
['`IOB_OUTPUT(', AXIL_DATA_W,      'axil_wdata',   'Write channel data'], \
['`IOB_OUTPUT(', AXIL_DATA_W+'/8', 'axil_wstrb',   'Write channel write strobe'], \
['`IOB_OUTPUT(', 1,                'axil_wvalid',  'Write channel valid'], \
['`IOB_INPUT(',  1,                'axil_wready',  'Write channel ready'], \
['`IOB_INPUT(',  AXI_ID_W,         'axil_bid',     'Write response channel ID'], \
['`IOB_INPUT(',  AXI_RESP_W,       'axil_bresp',   'Write response channel response'], \
['`IOB_INPUT(',  1,                'axil_bvalid',  'Write response channel valid'], \
['`IOB_OUTPUT(', 1,                'axil_bready',  'Write response channel ready'] \
]

def make_axil_read(AXIL_ADDR_W, AXIL_DATA_W):
    return [ \
['`IOB_OUTPUT(', AXI_ID_W,         'axil_arid',    'Address read channel ID'], \
['`IOB_OUTPUT(', AXIL_ADDR_W,      'axil_araddr',  'Address read channel address'], \
['`IOB_OUTPUT(', AXI_PROT_W,       'axil_arprot',  'Address read channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`IOB_OUTPUT(', AXI_QOS_W,        'axil_arqos',   'Address read channel quality of service'], \
['`IOB_OUTPUT(', 1,                'axil_arvalid', 'Address read channel valid'], \
['`IOB_INPUT(', 1,                 'axil_arready', 'Address read channel ready'], \
['`IOB_INPUT(', AXI_ID_W,          'axil_rid',     'Read channel ID'], \
['`IOB_INPUT(', AXIL_DATA_W,       'axil_rdata',   'Read channel data'], \
['`IOB_INPUT(', AXI_RESP_W,        'axil_rresp',   'Read channel response'], \
['`IOB_INPUT(', 1,                 'axil_rvalid',  'Read channel valid' ], \
['`IOB_OUTPUT(', 1,                'axil_rready',  'Read channel ready'] \
]

def make_axil(AXIL_ADDR_W, AXIL_DATA_W):
    return make_axil_write(AXIL_ADDR_W, AXIL_DATA_W) + make_axil_read(AXIL_ADDR_W, AXIL_DATA_W)


def reverse(direction):
    if direction == '`IOB_INPUT(':
        return '`IOB_OUTPUT('
    elif direction == '`IOB_OUTPUT(':
        return '`IOB_INPUT('
    else:
        print("ERROR: reverse_direction : invalid argument")
        quit()
        
def tbsignal(direction):
    if direction == '`IOB_INPUT(':
        return '`IOB_WIRE('
    elif direction == '`IOB_OUTPUT(':
        return '`IOB_VAR('
    else:
        print("ERROR: tb_reciprocal : invalid argument")
        quit()

#
# Port
#

def axi_m_port(prefix, fout):
    for i in range(len(axi_m)):
        try: width = str(int(axi_m[i][1]));
        except: width = axi_m[i][1];
        fout.write(' '+axi_m[i][0]+prefix+axi_m[i][2]+', '+width+'), //'+axi_m[i][3]+'\n')
    
def axi_s_port(prefix, fout):
    for i in range(len(axi_m)):
        try: width = str(int(axi_m[i][1]));
        except: width = axi_m[i][1];
        fout.write(' '+reverse(axi_m[i][0])+prefix+axi_m[i][2]+', '+width+'), //'+axi_m[i][3]+'\n')

#
# Portmap
#

def axi_portmap(port_prefix, wire_prefix, fout):
    for i in range(len(axi_m)):
        try: width = str(int(axi_m[i][1]));
        except: width = axi_m[i][1];
        fout.write('.'+port_prefix+axi_m[i][2]+'('+wire_prefix+axi_m[i][2]+'), //'+axi_m[i][3]+'\n')

#
# Wire
#

def axi_m_tb(prefix, fout):
    for i in range(len(axi_m)):
        try: width = str(int(axi_m[i][1]));
        except: width = axi_m[i][1];
        fout.write(tbsignal(axi_m[i][0])+prefix+axi_m[i][2]+', '+width+') //'+axi_m[i][3]+'\n')
    
def axi_s_tb(prefix, fout):
    for i in range(len(axi_m)):
        try: width = str(int(axi_m[i][1]));
        except: width = axi_m[i][1];
        fout.write(tbsignal(reverse(axi_m[i][0]))+prefix+axi_m[i][2]+', '+width+') //'+axi_m[i][3]+'\n')

def axi_wire(prefix, fout):
    for i in range(len(axi_m)):
        try: width = str(int(axi_m[i][1]));
        except: width = axi_m[i][1];
        fout.write('`IOB_WIRE('+prefix+axi_m[i][2]+', '+width+') //'+axi_m[i][3]+'\n')

#
# Main
#
        
def main ():

    # parse command line arguments
    if len(sys.argv) < 4 or len(sys.argv) > 6:
        print(len(sys.argv))
        print("Usage:  ./axi_gen.py type addr_w data_w [port_prefix wire_prefix]")
        quit()

    #axi bus type
    typ = sys.argv[1]

    #address width
    ADDR_W = sys.argv[2]

    #data width
    DATA_W = sys.argv[3]

    #port and wire prefix
    port_prefix = ''
    wire_prefix = ''
    if len(sys.argv) > 4: port_prefix = sys.argv[4]
    if len(sys.argv) > 5: wire_prefix = sys.argv[5]

    # open output .vh file
    fout = open (port_prefix+wire_prefix+typ+".vh", 'w')

    # make AXI bus
    global axi_m
    if (typ.find("axi_write_")>=0): axi_m = make_axi_write(ADDR_W, DATA_W)
    elif (typ.find("axi_read_")>=0): axi_m = make_axi_read(ADDR_W, DATA_W)
    elif (typ.find("axi_")>=0): axi_m = make_axi(ADDR_W, DATA_W)
    elif (typ.find("axil_write_")>=0): axi_m = make_axil_write(ADDR_W, DATA_W)
    elif (typ.find("axil_read_")>=0): axi_m = make_axil_read(ADDR_W, DATA_W)
    elif (typ.find("axil_")>=0): axi_m = make_axil(ADDR_W, DATA_W)

    typ = typ.replace("write_","")
    typ = typ.replace("read_","")

    if (typ.find("m_port")+1 or typ.find("s_port")+1):
        fout.write('  //START_IO_TABLE '+port_prefix+typ+'\n')

    # call function func to generate .vh file
    func = typ.replace("axil_","axi_")
    if (typ.find("portmap")+1): eval(func+"('"+port_prefix+"','"+wire_prefix+"', fout)")
    else: eval(func+"('"+port_prefix+"', fout)")

if __name__ == "__main__" : main ()
