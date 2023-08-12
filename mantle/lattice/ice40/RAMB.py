from collections import OrderedDict
import hwtypes as ht
import magma as m
#from .simulation import gen_sb_ram40_4k_sim

__all__  = ['SB_RAM40_4K']

__all__ += ['RAMB', 'ROMB']

# posedge read clock, posedge write clock
class SB_RAM40_4K(m.Circuit):
    io = m.IO(
        RDATA=m.Out(m.Bits[ 16 ]),
        RADDR=m.In(m.Bits[ 11 ]),
        RCLK= m.In(m.Clock),
        RCLKE=m.In(m.Enable),
        RE=   m.In(m.Enable),
        WCLK= m.In(m.Clock),
        WCLKE=m.In(m.Enable),
        WE=   m.In(m.Enable),
        WADDR=m.In(m.Bits[ 11 ]),
        MASK= m.In(m.Bits[ 16 ]),
        WDATA=m.In(m.Bits[ 16 ])
    )
    param_types = {
        "WRITE_MODE": ht.BitVector[2],
        "READ_MODE":  ht.BitVector[2],
        "INIT_0": ht.BitVector[256],
        "INIT_1": ht.BitVector[256],
        "INIT_2": ht.BitVector[256],
        "INIT_3": ht.BitVector[256],
        "INIT_4": ht.BitVector[256],
        "INIT_5": ht.BitVector[256],
        "INIT_6": ht.BitVector[256],
        "INIT_7": ht.BitVector[256],
        "INIT_8": ht.BitVector[256],
        "INIT_9": ht.BitVector[256],
        "INIT_A": ht.BitVector[256],
        "INIT_B": ht.BitVector[256],
        "INIT_C": ht.BitVector[256],
        "INIT_D": ht.BitVector[256],
        "INIT_E": ht.BitVector[256],
        "INIT_F": ht.BitVector[256] 
    }
    #stateful=True,
    #simulate=gen_sb_ram40_4k_sim(prc=True, pwc=True),
    #coreir_lib='ice40'


# posedge read clock, negedge write clock
# negedge read clock, posedge write clock
# negedge read clock, negedge write clock
# - can get these effects by inverting the RCLK and/or the WCLK
# NEGCLK_R(0|1)
# NEGCLK_W(0|1)


# MASK=0, write-enabled, MASK=1, write-disabled

#
# N is the number of bits of output
#
def init(rom,N,mode=0):
    # INIT_%x 256 bits = 32 bytes = 64 nibbles
    params = OrderedDict({})
    params['WRITE_MODE'] = mode
    params['READ_MODE'] = mode

    # M is the number of high (>8) address values
    #  e.g. if N == 8, then there are 2 high address values
    M = 16//N
    for i in range(16):
        v = 0
        for b in range(256):
            col = (b//M)%N
            # NB. the high address values ocuppy the lowest bit positions
            row = 256*(b%M) + 16*i + b//16
            bit = (rom[row] >> col)&1
            #print('i=%x'%i, 'b=%d'%b, row, col)
            v |= bit << b
        key = 'INIT_%X' % i
        #params[key] = "256'h%064x" % v
        params[key] = (v, 256)
    return params

def wireaddr(addr, n):
    for i in range(n):
        m.wire(0, addr[10-i])
    return addr[0:11-n]

def _RAMB(height, width, rom=None, readonly=False):
    if not rom:
        rom = height * [0]
    n = len(rom)
    assert height == n

    ram40 = None
    if   n ==  256: # 256x16
        assert width == 16
        params = init(rom,16,mode=0)
        ram40 = SB_RAM40_4K(**params)
        ram40.RADDR = wireaddr(ram40.RADDR, 3)
        if not readonly:
            ram40.WADDR = wireaddr(ram40.WADDR, 3)
    elif n ==  512: # 512x8
        assert width == 8
        params = init(rom,8,mode=1)
        ram40 = SB_RAM40_4K(**params)
        ram40.RADDR = wireaddr(ram40.RADDR, 2)
        RDATA = ram40.RDATA
        ram40.RDATA = m.array([RDATA[0], RDATA[2], RDATA[4], RDATA[6],
                            RDATA[8], RDATA[10], RDATA[12], RDATA[14]])
        if not readonly:
            WDATA = ram40.WDATA
            m.wire(0,WDATA[1])
            m.wire(0,WDATA[3])
            m.wire(0,WDATA[5])
            m.wire(0,WDATA[7])
            m.wire(0,WDATA[9])
            m.wire(0,WDATA[11])
            m.wire(0,WDATA[13])
            m.wire(0,WDATA[15])
            ram40.WDATA = m.array([WDATA[0], WDATA[2], WDATA[4], WDATA[6],
                                WDATA[8], WDATA[10], WDATA[12], WDATA[14]])
            ram40.WADDR = wireaddr(ram40.WADDR, 2)
    elif n == 1024: # 1024x4
        assert width == 4
        params = init(rom,4,mode=2)
        ram40 =  SB_RAM40_4K(**params)
        ram40.RADDR = wireaddr(ram40.RADDR, 1)
        RDATA = ram40.RDATA
        ram40.RDATA = m.array([RDATA[1], RDATA[5], RDATA[9], RDATA[13]])
        if not readonly:
            WDATA = ram40.WDATA
            m.wire(0,WDATA[0])
            m.wire(0,WDATA[2])
            m.wire(0,WDATA[3])
            m.wire(0,WDATA[4])
            m.wire(0,WDATA[6])
            m.wire(0,WDATA[7])
            m.wire(0,WDATA[8])
            m.wire(0,WDATA[10])
            m.wire(0,WDATA[11])
            m.wire(0,WDATA[12])
            m.wire(0,WDATA[14])
            m.wire(0,WDATA[15])
            ram40.WDATA = m.array([WDATA[1], WDATA[5], WDATA[9], WDATA[13]])
            ram40.WADDR = wireaddr(ram40.WADDR, 1)
    elif n == 2048: # 2048x2
        assert width == 2
        params = init(rom,2,mode=3)
        ram40 = SB_RAM40_4K(**params)
        RDATA = ram40.RDATA
        ram40.RDATA = m.array([RDATA[3], RDATA[11]])
        if not readonly:
            WDATA = ram40.WDATA
            m.wire(0,WDATA[0])
            m.wire(0,WDATA[1])
            m.wire(0,WDATA[2])
            m.wire(0,WDATA[4])
            m.wire(0,WDATA[5])
            m.wire(0,WDATA[6])
            m.wire(0,WDATA[7])
            m.wire(0,WDATA[8])
            m.wire(0,WDATA[9])
            m.wire(0,WDATA[10])
            m.wire(0,WDATA[12])
            m.wire(0,WDATA[13])
            m.wire(0,WDATA[14])
            m.wire(0,WDATA[15])
            ram40.WDATA = m.array([WDATA[3], WDATA[11]])

    if readonly:
        m.wire( m.enable(0), ram40.WE    )
        m.wire( m.array(11*[0]), ram40.WADDR )
        m.wire( m.array(16*[0]), ram40.WDATA )
    m.wire(m.enable(0 if readonly else 1), ram40.WCLKE )
    m.wire(m.enable(1), ram40.RCLKE)
    m.wire(m.array(16*[0]), ram40.MASK)
    if readonly:
        return m.AnonymousCircuit("RADDR", ram40.RADDR,
                                "RDATA", ram40.RDATA,
                                "RCLK",  ram40.RCLK,
                                "RE",    ram40.RE)
    else:
        return m.AnonymousCircuit("RADDR", ram40.RADDR,
                                "RDATA", ram40.RDATA,
                                "RCLK",  ram40.RCLK,
                                "RE",    ram40.RE,
                                "WADDR", ram40.WADDR,
                                "WDATA", ram40.WDATA,
                                "WCLK",  ram40.WCLK,
                                "WE",    ram40.WE)

def RAMB(height, width, ram=None):
    return _RAMB(height, width, ram, readonly=False)

def ROMB(height, width, rom=None):
    return _RAMB(height, width, rom, readonly=True)
