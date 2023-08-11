import pytest
import magma as m
from magma.testing.utils import check_gold
from .simulation import simulate_sb_carry

# Implements (I0&I1)|(I1&I2)|(I2&I0)
SB_CARRY = m.DeclareCircuit('SB_CARRY',
               "I0", m.In(m.Bit), # must be the same as SB_LUT4 I1 to pack
               "I1", m.In(m.Bit), # must be the same as SB_LUT4 I2 to pack
               "CI", m.In(m.Bit), # must be from previous SB_LUT4 to pack
               "CO", m.Out(m.Bit),
               stateful=False,
               simulate=simulate_sb_carry,
               coreir_lib="ice40")


@pytest.mark.skip()
def test_declare():
    class Main(m.Circuit):
        io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            I2=m.In(m.Bit),
            O=m.Out(m.Bit)
        )
        sb_carry = SB_CARRY()
        sb_carry.I0 @= io.I0
        sb_carry.I1 @= io.I1
        sb_carry.CI @= io.I2
        io.O @= sb_carry.CO

    m.compile("build/test_declare", Main, output="mlir-verilog")
    assert check_gold(__file__, "test_declare.v")
