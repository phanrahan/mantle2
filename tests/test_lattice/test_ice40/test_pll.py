import magma as m
from check import check_ice40

from mantle.lattice.ice40.PLL import SB_PLL


def test_pll():

    class Top(m.Circuit):
        io = m.IO(
            REFERENCECLK=m.In(m.Clock),
            RESETB=m.In(m.Bit),
            BYPASS=m.In(m.Bit),
            PLLOUTCORE=m.Out(m.Bit),
            PLLOUTGLOBAL=m.Out(m.Clock)
        )
        pll = SB_PLL(32000000, 16000000)
        pll.REFERENCECLK @= io.REFERENCECLK
        pll.RESETB @= io.RESETB
        pll.BYPASS @= io.BYPASS
        io.PLLOUTCORE @= pll.PLLOUTCORE
        io.PLLOUTGLOBAL @= pll.PLLOUTGLOBAL

    check_ice40(__file__, 'test_pll', Top)
