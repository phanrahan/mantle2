import pytest
from hwtypes import BitVector
import magma as m
from magma.testing.utils import check_gold

from mantle.lattice.ice40.RAMB import ROMB, RAMB



def test_romb():
    main = m.DefineCircuit("main",
                         "RDATAOUT", m.Out(m.Bits[ 8 ]),
                         "CLK", m.In(m.Clock)) # FIXME: hack
    romb = ROMB(512, 8, [0b00000001, 0b11111111] + [0] * 510)
    m.wire(romb.RADDR, m.uint(1, 9))
    m.wire(romb.RCLK, main.CLK)
    m.wire(romb.RE, m.enable(1))

    m.wire(romb.RDATA, main.RDATAOUT)
    m.EndCircuit()

    m.compile("build/test_romb", main, output="mlir-verilog")
    assert check_gold(__file__, "test_romb.v")

    #sim = PythonSimulator(main, clock=main.CLK)
    #sim.evaluate()

    #sim.advance(2)

    #assert BitVector[8](sim.get_value(main.RDATAOUT)) == BitVector[8](0b11111111)


def test_ramb():
    main = m.DefineCircuit("main",
                         "RDATA", m.Out(m.Bits[ 8 ]),
                         "WDATA", m.In(m.Bits[ 8 ]),
                         "WE",   m.In(m.Enable),
                         "CLK", m.In(m.Clock))
    ramb = RAMB(512, 8, [0b00000001, 0b11111111] + [0] * 510)
    m.wire(ramb.RADDR, m.uint(1, 9))
    m.wire(ramb.RCLK, main.CLK)
    m.wire(ramb.RE, m.enable(1))
    m.wire(ramb.WADDR, m.uint(1, 9))
    m.wire(ramb.WCLK, main.CLK)
    m.wire(ramb.WE, main.WE)

    m.wire(ramb.RDATA, main.RDATA)
    m.wire(ramb.WDATA, main.WDATA)
    m.EndCircuit()

    m.compile("build/test_ramb", main, output="mlir-verilog")
    assert check_gold(__file__, "test_ramb.v")

    #sim = PythonSimulator(main, clock=main.CLK)
    #sim.set_value(main.WE, False)
    #sim.evaluate()

    #sim.advance(2)

    #assert BitVector[8](sim.get_value(main.RDATA)) == BitVector[8](0b11111111)

    # Write 0xBE to WADDR = 1
    #sim.set_value(main.WE, True)
    #sim.set_value(main.WDATA, BitVector[8](0xBE))

    #sim.advance(2)

    # Read RADDR = 1 again
    #sim.set_value(main.WE, False)
    #sim.evaluate()

    #sim.advance(2)

    #assert BitVector[8](sim.get_value(main.RDATA)) == BitVector[8](0xBE)

