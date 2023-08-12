import magma as m
from mantle.lattice.ice40.DFF import DFF
from magma.testing.utils import check_gold


def test_dff():

    class Top(m.Circuit):
        io = m.IO(
            C=m.In(m.Clock),
            D=m.In(m.Bit),
            Q=m.Out(m.Bit),
        )
        io.Q @= DFF()(io.D)

    m.compile("build/test_dff", Top, output="mlir-verilog")
    assert check_gold(__file__, "test_dff.v")
