import operator

import magma as m
from mantle.lattice.ice40.PLB import A0, A1, A2, A3, SB_LUT4
from mantle.lattice.ice40.LUT import LUT1, LUT2, LUT3, LUT4


def test_lut1():
    lut = LUT1(A0)
    assert all(map(operator.is_, lut.interface.outputs(), (lut.I0,)))
    assert all(map(operator.is_, lut.interface.inputs(), (lut.O,)))
    assert len(lut.instances) == 1
    assert isinstance(lut.instances[0], SB_LUT4)
    assert lut.instances[0].kwargs == {"LUT_INIT": A0}

def test_lut2():
    lut = LUT2(A0 ^ A1)
    assert all(map(operator.is_, lut.interface.outputs(), (lut.I0, lut.I1)))
    assert all(map(operator.is_, lut.interface.inputs(), (lut.O,)))
    assert len(lut.instances) == 1
    assert isinstance(lut.instances[0], SB_LUT4)
    assert lut.instances[0].kwargs == {"LUT_INIT": A0 ^ A1}


def test_lut3():
    lut = LUT3(A0 ^ A1 ^ A2)
    assert all(
        map(operator.is_, lut.interface.outputs(), (lut.I0, lut.I1, lut.I2))
    )
    assert all(map(operator.is_, lut.interface.inputs(), (lut.O,)))
    assert len(lut.instances) == 1
    assert isinstance(lut.instances[0], SB_LUT4)
    assert lut.instances[0].kwargs == {"LUT_INIT": A0 ^ A1 ^ A2}

def test_lut4():
    lut = LUT4(A0 ^ A1 ^ A2 ^ A3) 
    assert all(
        map(operator.is_, lut.interface.outputs(), (lut.I0, lut.I1, lut.I2, lut.I3))
    )
    assert all(map(operator.is_, lut.interface.inputs(), (lut.O,)))
    assert len(lut.instances) == 1
    assert isinstance(lut.instances[0], SB_LUT4)
    assert lut.instances[0].kwargs == {"LUT_INIT": A0 ^ A1 ^ A2 ^ A3}
