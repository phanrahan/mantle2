import hwtypes as ht
import magma as m
from check import check_ice40

from mantle.lattice.ice40.PLB import SB_LUT4, SB_CARRY, SB_DFF


def test_sb_lut4():

    class Top(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            I2=m.In(m.Bit),
            I3=m.In(m.Bit),
            O=m.Out(m.Bit)
        )
        io.O @= SB_LUT4(LUT_INIT=ht.BitVector[16](0xBEEF))(
            io.I0,
            io.I1,
            io.I2,
            io.I3
        )

    check_ice40(__file__, 'test_sb_lut4', Top)

def test_sb_carry():

    class Top(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            I2=m.In(m.Bit),
            CI=m.In(m.Bit),
            CO=m.Out(m.Bit)
        )
        io.CO @= SB_CARRY()(io.I0, io.I1, io.CI)

    check_ice40(__file__, 'test_sb_carry', Top)


def test_sb_dff():

    class Top(m.Circuit):
        io = m.IO(
            C=m.In(m.Clock),
            D=m.In(m.Bit),
            Q=m.Out(m.Bit),
        )
        io.Q @= SB_DFF()(io.D)

    check_ice40(__file__, 'test_sb_dff', Top)
