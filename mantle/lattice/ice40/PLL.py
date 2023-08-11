import magma as m

__all__ = ['SB_PLL', 'SB_PLL40_CORE']


class SB_PLL40_CORE(m.Circuit):
    io = m.IO(
        REFERENCECLK=m.In(m.Clock),
        RESETB=m.In(m.Bit),
        BYPASS=m.In(m.Bit),
        PLLOUTCORE=m.Out(m.Bit),
        PLLOUTGLOBAL=m.Out(m.Clock)
        #coreir_lib='ice40'
    )

class SB_PLL(m.Generator2):

    """Instantiate a PLL"""
    def __init__( self, freqout, freqin=12000000 ):

        self.io = m.IO( I=m.In(m.Bit), O=m.Out(m.Bit) )

        divr, divf, divq, filter = findparams(freqin, freqout)

        params = {}
        params["FEEDBACK_PATH"] = "SIMPLE"
        params["PLLOUT_SELECT"] = "GENCLK"
        # Reference clock divider (div+1) [0, ..., 15]
        params["DIVR"] = (divr, 4)
        # Feedback divider (div+1) [0, ..., 63]
        params["DIVF"] = (divf, 7)
        # VCO divider (divq+1) [0, ..., 6]
        params["DIVQ"] = (divq, 3)
        params["FILTER_RANGE"] = (filter, 3)

        pll = SB_PLL40_CORE(**params)

        m.wire(1, pll.RESETB)
        m.wire(0, pll.BYPASS)
        pll.REFERENCECLK @= self.io.I
        self.io.O = pll.PLLOUTGLOBAL

def filterrange(freqin, divr, divf):
    pfd = freqin / (divr + 1)
    vco = pfd * (divf + 1)

    if   pfd <  17: range = 1
    elif pfd <  26: range = 2
    elif pfd <  44: range = 3
    elif pfd <  66: range = 4
    elif pfd < 101: range = 5
    else:           range = 6

    return range

def findparams(freqin, freqout):
    freqin  /= 1000000
    freqout /= 1000000

    bestfreqout = 0.
    for divr in range(16):
        pfd = freqin / (divr + 1)
        if pfd < 10 or pfd > 133:
            continue

        for divf in range(64):
            vco = pfd * (divf + 1)
            if vco < 533 or vco > 1066:
                continue

            # The valid range for DIVQ is 1..6. 
            #
            # This is correctly documented in the ICE Technology Library 
            # Document, but unfortunately incorrectly documented as 0..7 
            # in the iCE40 sysCLOCK PLL Design and Usage Guide.
            #
            for divq in range(1,7):
                fout = vco / (1 << divq)

                # simple mode

                #print('pfd=',pfd, '(divr=',divr+1,')')
                #print('vco=',vco, '(mulf=',divf+1,')')
                #print('freqout=',fout, '(divq=',divq,1<<divq,')')
                if abs(fout - freqout) < abs(bestfreqout - freqout):
                    bestdivr = divr
                    bestdivf = divf
                    bestdivq = divq
                    bestfreqout = fout
                    #print('pfd=',pfd, '(divr=',bestdivr+1,')')
                    #print('vco=',vco, '(mulf=',bestdivf+1,')')
                    #print('bestfreqout=',bestfreqout, '(divq=',bestdivq,1<<bestdivq,')')
    return bestdivr, bestdivf, bestdivq, filterrange(freqin, bestdivr, bestdivf)

#
# from swapforth
#
#  SB_PLL40_CORE #(.FEEDBACK_PATH("SIMPLE"),
#                  .PLLOUT_SELECT("GENCLK"),
#                  .DIVR(4'b0000),
#                  .DIVF(7'd3),
#                  .DIVQ(3'b000),
#                  .FILTER_RANGE(3'b001),
#                 ) uut (
#                         .REFERENCECLK(pclk),
#                         .PLLOUTCORE(clk),
#                         //.PLLOUTGLOBAL(clk),
#                         // .LOCK(D5),
#                         .RESETB(1'b1),
#                         .BYPASS(1'b0)
#                        );


if __name__ == '__main__':
    d = m.DefineCircuit('main', "CLKIN", In(Bit), "CLKOUT", Out(Bit))
    pll = SB_PLL(25000000, 12000000)
    m.wire(d.CLKIN, pll.I)
    m.wire(pll.O, d.CLKOUT)
    m.EndCircuit()
