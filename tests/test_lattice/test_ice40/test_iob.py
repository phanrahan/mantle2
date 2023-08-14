import pytest
import magma as m
from check import check_ice40

from mantle.lattice.ice40.IOB import SB_IO


@pytest.mark.skip()
def test_sb_io():

    class Top(m.Circuit):
        io = m.IO(
            PACKAGE_PIN=m.In(m.Bit),
            D_IN_0=m.In(m.Bit),
            D_OUT_0=m.Out(m.Bit)
        )
        iob = SB_IO()
        iob.PACKAGE_PIN @= io.PACKAGE_PIN
        io.D_OUT_0 @= iob.D_OUT_0

    check_ice40(__file__, 'test_io', Top)

