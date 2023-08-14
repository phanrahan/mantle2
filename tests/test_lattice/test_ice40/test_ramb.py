import pytest
from hwtypes import BitVector
import magma as m
from check import check_ice40

from mantle.lattice.ice40.RAMB import ROMB, RAMB



def test_romb():
    Top = m.DefineCircuit("Top",
                         "RDATAOUT", m.Out(m.Bits[ 8 ]),
                         "CLK", m.In(m.Clock)) # FIXME: hack
    romb = ROMB(512, 8, [0b00000001, 0b11111111] + [0] * 510)
    m.wire(romb.RADDR, m.uint(1, 9))
    m.wire(romb.RCLK, Top.CLK)
    m.wire(romb.RE, m.enable(1))

    m.wire(romb.RDATA, Top.RDATAOUT)
    m.EndCircuit()

    check_ice40(__file__, 'test_romb', Top)

    #sim = PythonSimulator(Top, clock=Top.CLK)
    #sim.evaluate()

    #sim.advance(2)

    #assert BitVector[8](sim.get_value(Top.RDATAOUT)) == BitVector[8](0b11111111)


def test_ramb():
    Top = m.DefineCircuit("Top",
                         "RDATA", m.Out(m.Bits[ 8 ]),
                         "WDATA", m.In(m.Bits[ 8 ]),
                         "WE",   m.In(m.Enable),
                         "CLK", m.In(m.Clock))
    ramb = RAMB(512, 8, [0b00000001, 0b11111111] + [0] * 510)
    m.wire(ramb.RADDR, m.uint(1, 9))
    m.wire(ramb.RCLK, Top.CLK)
    m.wire(ramb.RE, m.enable(1))
    m.wire(ramb.WADDR, m.uint(1, 9))
    m.wire(ramb.WCLK, Top.CLK)
    m.wire(ramb.WE, Top.WE)

    m.wire(ramb.RDATA, Top.RDATA)
    m.wire(ramb.WDATA, Top.WDATA)
    m.EndCircuit()

    check_ice40(__file__, 'test_ramb', Top)


    #sim = PythonSimulator(Top, clock=Top.CLK)
    #sim.set_value(Top.WE, False)
    #sim.evaluate()

    #sim.advance(2)

    #assert BitVector[8](sim.get_value(Top.RDATA)) == BitVector[8](0b11111111)

    # Write 0xBE to WADDR = 1
    #sim.set_value(Top.WE, True)
    #sim.set_value(Top.WDATA, BitVector[8](0xBE))

    #sim.advance(2)

    # Read RADDR = 1 again
    #sim.set_value(Top.WE, False)
    #sim.evaluate()

    #sim.advance(2)

    #assert BitVector[8](sim.get_value(Top.RDATA)) == BitVector[8](0xBE)

