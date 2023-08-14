import magma as m
from check import check_ice40

from mantle.lattice.ice40.DFF import DFF


def test_dff():

    class Top(m.Circuit):
        io = m.IO(
            C=m.In(m.Clock),
            D=m.In(m.Bit),
            Q=m.Out(m.Bit),
        )
        io.Q @= DFF()(io.D, io.C)

    check_ice40(__file__, 'test_dff', Top)
