#!/usr/bin/python3

#
# ./axi_gen.py prefix prefix2 typ
#
# typ = [master|slave]_[port|portmap|wire|tb] or [master|slave]_[write|read]_[port|portmap|wire|tb]

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
['`OUTPUT(', AXI_ID_W,        'axi_awid',    'Address write channel ID'], \
['`OUTPUT(', AXI_ADDR_W,      'axi_awaddr',  'Address write channel address'], \
['`OUTPUT(', AXI_LEN_W,       'axi_awlen',   'Address write channel burst length'], \
['`OUTPUT(', AXI_SIZE_W,      'axi_awsize',  'Address write channel burst size. This signal indicates the size of each transfer in the burst'], \
['`OUTPUT(', AXI_BURST_W,     'axi_awburst', 'Address write channel burst type'], \
['`OUTPUT(', AXI_LOCK_W,      'axi_awlock',  'Address write channel lock type'], \
['`OUTPUT(', AXI_CACHE_W,     'axi_awcache', 'Address write channel memory type. Transactions set with Normal Non-cacheable Modifiable and Bufferable (0011).'], \
['`OUTPUT(', AXI_PROT_W,      'axi_awprot',  'Address write channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`OUTPUT(', AXI_QOS_W,       'axi_awqos',   'Address write channel quality of service'], \
['`OUTPUT(', 1,               'axi_awvalid', 'Address write channel valid'], \
['`INPUT(',  1,               'axi_awready', 'Address write channel ready'], \
['`OUTPUT(', AXI_ID_W,        'axi_wid',     'Write channel ID'], \
['`OUTPUT(', AXI_DATA_W,      'axi_wdata',   'Write channel data'], \
['`OUTPUT(', AXI_DATA_W+'/8', 'axi_wstrb',   'Write channel write strobe'], \
['`OUTPUT(', 1,               'axi_wlast',   'Write channel last word flag'], \
['`OUTPUT(', 1,               'axi_wvalid',  'Write channel valid'], \
['`INPUT(',  1,               'axi_wready',  'Write channel ready'], \
['`INPUT(',  AXI_ID_W,        'axi_bid',     'Write response channel ID'], \
['`INPUT(',  AXI_RESP_W,      'axi_bresp',   'Write response channel response'], \
['`INPUT(',  1,               'axi_bvalid',  'Write response channel valid'], \
['`OUTPUT(', 1,               'axi_bready',  'Write response channel ready'] \
]

def make_axi_read(AXI_ADDR_W, AXI_DATA_W):
    return [ \
['`OUTPUT(', AXI_ID_W,        'axi_arid',    'Address read channel ID'], \
['`OUTPUT(', AXI_ADDR_W,      'axi_araddr',  'Address read channel address'], \
['`OUTPUT(', AXI_LEN_W,       'axi_arlen',   'Address read channel burst length'], \
['`OUTPUT(', AXI_SIZE_W,      'axi_arsize',  'Address read channel burst size. This signal indicates the size of each transfer in the burst'], \
['`OUTPUT(', AXI_BURST_W,     'axi_arburst', 'Address read channel burst type'], \
['`OUTPUT(', AXI_LOCK_W,      'axi_arlock',  'Address read channel lock type'], \
['`OUTPUT(', AXI_CACHE_W,     'axi_arcache', 'Address read channel memory type. Transactions set with Normal Non-cacheable Modifiable and Bufferable (0011).'], \
['`OUTPUT(', AXI_PROT_W,      'axi_arprot',  'Address read channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`OUTPUT(', AXI_QOS_W,       'axi_arqos',   'Address read channel quality of service'], \
['`OUTPUT(', 1,               'axi_arvalid', 'Address read channel valid'], \
['`INPUT(',  1,               'axi_arready', 'Address read channel ready'], \
['`INPUT(',  AXI_ID_W,        'axi_rid',     'Read channel ID'], \
['`INPUT(',  AXI_DATA_W,      'axi_rdata',   'Read channel data'], \
['`INPUT(',  AXI_RESP_W,      'axi_rresp',   'Read channel response'], \
['`INPUT(',  1,               'axi_rlast',   'Read channel last word'], \
['`INPUT(',  1,               'axi_rvalid',  'Read channel valid' ], \
['`OUTPUT(', 1,               'axi_rready' , 'Read channel ready'] \
]

def make_axi(AXI_ADDR_W, AXI_DATA_W):
    return make_axi_write(AXI_ADDR_W, AXI_DATA_W) + make_axi_read(AXI_ADDR_W, AXI_DATA_W)

#
# AXI-4 Lite
#

def make_axil_write(AXIL_ADDR_W, AXIL_DATA_W):
    return [ \
['`OUTPUT(', AXI_ID_W,         'axil_awid',    'Address write channel ID'], \
['`OUTPUT(', AXIL_ADDR_W,      'axil_awaddr',  'Address write channel address'], \
['`OUTPUT(', AXI_PROT_W,       'axil_awprot',  'Address write channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`OUTPUT(', AXI_QOS_W,        'axil_awqos',   'Address write channel quality of service'], \
['`OUTPUT(', 1,                'axil_awvalid', 'Address write channel valid'], \
['`INPUT(',  1,                'axil_awready', 'Address write channel ready'], \
['`OUTPUT(', AXI_ID_W,         'axil_wid',     'Write channel ID'], \
['`OUTPUT(', AXIL_DATA_W,      'axil_wdata',   'Write channel data'], \
['`OUTPUT(', AXIL_DATA_W+'/8', 'axil_wstrb',   'Write channel write strobe'], \
['`OUTPUT(', 1,                'axil_wvalid',  'Write channel valid'], \
['`INPUT(',  1,                'axil_wready',  'Write channel ready'], \
['`INPUT(',  AXI_ID_W,         'axil_bid',     'Write response channel ID'], \
['`INPUT(',  AXI_RESP_W,       'axil_bresp',   'Write response channel response'], \
['`INPUT(',  1,                'axil_bvalid',  'Write response channel valid'], \
['`OUTPUT(', 1,                'axil_bready',  'Write response channel ready'] \
]

def make_axil_read(AXIL_ADDR_W, AXIL_DATA_W):
    return [ \
['`OUTPUT(', AXI_ID_W,         'axil_arid',    'Address read channel ID'], \
['`OUTPUT(', AXIL_ADDR_W,      'axil_araddr',  'Address read channel address'], \
['`OUTPUT(', AXI_PROT_W,       'axil_arprot',  'Address read channel protection type. Transactions set with Normal, Secure, and Data attributes (000).'], \
['`OUTPUT(', AXI_QOS_W,        'axil_arqos',   'Address read channel quality of service'], \
['`OUTPUT(', 1,                'axil_arvalid', 'Address read channel valid'], \
['`INPUT(', 1,                 'axil_arready', 'Address read channel ready'], \
['`INPUT(', AXI_ID_W,          'axil_rid',     'Read channel ID'], \
['`INPUT(', AXIL_DATA_W,       'axil_rdata',   'Read channel data'], \
['`INPUT(', AXI_RESP_W,        'axil_rresp',   'Read channel response'], \
['`INPUT(', 1,                 'axil_rvalid',  'Read channel valid' ], \
['`OUTPUT(', 1,                'axil_rready',  'Read channel ready'] \
]

def make_axil(AXIL_ADDR_W, AXIL_DATA_W):
    return make_axil_write(AXIL_ADDR_W, AXIL_DATA_W) + make_axil_read(AXIL_ADDR_W, AXIL_DATA_W)


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
        fout.write('`WIRE('+prefix+axi_m[i][2]+', '+width+') //'+axi_m[i][3]+'\n')

def main ():

    # parse command line arguments
    if len(sys.argv) < 3 or len(sys.argv) > 6:
        print(len(sys.argv))
        print("Usage:  ./axi_gen.py prefix prefix2 typ aw dw")
        quit()
        
    if len(sys.argv) > 4:
        try:
            ADDR_W = int(sys.argv[4])
        except:
            ADDR_W = sys.argv[4]

    if len(sys.argv) > 5:
        try:
            DATA_W = int(sys.argv[5])
        except:
            DATA_W = sys.argv[5]

    prefix = sys.argv[1]
    prefix2 = sys.argv[2]
    typ = sys.argv[3]

    # open output .vh file
    fout = open (prefix+prefix2+typ+".vh", 'w')

    # make AXI bus
    global axi_m
    if (typ.find("axi_write_")+1): axi_m = make_axi_write(ADDR_W, DATA_W)
    elif (typ.find("axi_read_")+1): axi_m = make_axi_read(ADDR_W, DATA_W)
    elif (typ.find("axi_")+1): axi_m = make_axi(ADDR_W, DATA_W)
    elif (typ.find("axil_write_")+1): axi_m = make_axil_write(ADDR_W, DATA_W)
    elif (typ.find("axil_read_")+1): axi_m = make_axil_read(ADDR_W, DATA_W)
    elif (typ.find("axil_")+1): axi_m = make_axil(ADDR_W, DATA_W)

    typ = typ.replace("write_","")
    typ = typ.replace("read_","")
    typ = typ.replace("axil_","axi_")

    if (typ.find("m_port")+1 or typ.find("s_port")+1):
        fout.write('  //START_IO_TABLE '+prefix+typ+'\n')

    # call function to generate .vh file
    if (typ.find("portmap")+1): eval(typ+"('"+prefix+"','"+prefix2+"', fout)")
    else: eval(typ+"('"+prefix+"', fout)")

if __name__ == "__main__" : main ()
