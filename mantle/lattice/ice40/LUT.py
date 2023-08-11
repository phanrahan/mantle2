from collections.abc import Sequence
from hwtypes import IntegerTypes, BitVector, seq2int
import magma as m
from .PLB import SB_LUT4, A0, A1, A2, A3

__all__  = ['LUT1', 'LUT2', 'LUT3', 'LUT4']
__all__ += ['LUT5', 'LUT6', 'LUT7', 'LUT8']
__all__ += ['LUTN', 'LUT']
__all__ += ['Mux2']

BV16 = BitVector[16]

def lutinit(val) -> BV16:
    if isinstance(val, Sequence):
        val = seg2int(val)
    return BV16(val)


"""
Convenience wrappers around SB_LUT4
"""

class LUT1(m.Generator2):
    def __init__(self, contents):
        self.io = m.IO(
            I0=m.In(m.Bit),
            O=m.Out(m.Bit),
        )
        self.io.O @= SB_LUT4(LUT_INIT=lutinit(contents))(
            self.io.I0,
            0,
            0,
            0
        )

class LUT2(m.Generator2):
    def __init__(self, contents):
        self.io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            O=m.Out(m.Bit),
        )
        self.io.O @= SB_LUT4(LUT_INIT=lutinit(contents))(
            self.io.I0,
            self.io.I1,
            0,
            0
        )


class LUT3(m.Generator2):
    def __init__(self, contents):
        self.io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            I2=m.In(m.Bit),
            O=m.Out(m.Bit),
        )
        self.io.O @= SB_LUT4(LUT_INIT=lutinit(contents))(
            self.io.I0,
            self.io.I1,
            self.io.I2,
            0
        )

class LUT4(m.Generator2):
    def __init__(self, contents):
        self.io = m.IO(
            I0=m.In(m.Bit),
            I1=m.In(m.Bit),
            I2=m.In(m.Bit),
            I3=m.In(m.Bit),
            O=m.Out(m.Bit),
        )
        self.io.O @= SB_LUT4(LUT_INIT=lutinit(contents))(
            self.io.I0,
            self.io.I1,
            self.io.I2,
            self.io.I3,
        )

def LUT5(rom, **kwargs):
    if isinstance(rom, IntegerTypes):
        rom = int2seq(rom, 32)
    I0, I1, I2, I3, I4 = m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)()
    lut = fork( LUT4(rom[ 0:16]), LUT4(rom[16:32]) )
    lut(I0, I1, I2, I3)
    mux = Mux2()
    mux(lut.O[0], lut.O[1], I4)
    return AnonymousCircuit("I0", I0,
                            "I1", I1,
                            "I2", I2,
                            "I3", I3,
                            "I4", I4,
                            "O", mux.O)


def LUT6(rom, **kwargs):
    if isinstance(rom, IntegerTypes):
        rom = int2seq(rom, 64)
    I0, I1, I2, I3, I4, I5 = m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)()
    lut = fork( LUT5(rom[ 0:32]), LUT5(rom[32:64]))
    mux = Mux2()
    lut(I0, I1, I2, I3, I4)
    mux(lut.O[0], lut.O[1], I5)
    return AnonymousCircuit("I0", I0,
                            "I1", I1,
                            "I2", I2,
                            "I3", I3,
                            "I4", I4,
                            "I5", I5,
                            "O", mux.O)

def LUT7(rom, **kwargs):
    if isinstance(rom, IntegerTypes):
        rom = int2seq(rom, 128)
    I0, I1, I2, I3, I4, I5, I6 = m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)()
    lut = fork( LUT6(rom[ 0:64]), LUT6(rom[64:128]))
    mux = Mux2()
    lut(I0, I1, I2, I3, I4, I5)
    mux(lut.O[0], lut.O[1], I6)
    return AnonymousCircuit("I0", I0,
                            "I1", I1,
                            "I2", I2,
                            "I3", I3,
                            "I4", I4,
                            "I5", I5,
                            "I6", I6,
                            "O", mux.O)

def LUT8(rom, **kwargs):
    if isinstance(rom, IntegerTypes):
        rom = int2seq(rom, 256)
    I0, I1, I2, I3, I4, I5, I6, I7 = m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)(), m.In(m.Bit)()
    lut = fork( LUT7(rom[ 0:128]), LUT7(rom[128:256]))
    mux = Mux2()
    lut(I0, I1, I2, I3, I4, I5, I6)
    mux(lut.O[0], lut.O[1], I7)
    return AnonymousCircuit("I0", I0,
                            "I1", I1,
                            "I2", I2,
                            "I3", I3,
                            "I4", I4,
                            "I5", I5,
                            "I6", I6,
                            "I7", I7,
                            "O", mux.O)

def LUTN(rom, n=None, **kwargs):
    """
    n-bit LUT

    I : In(Bits(n)), O : Out(Bit)
    """

    if n is not None:
        n = 1 << n

    if isinstance(rom, Sequence):
        if n is None:
            n = len(rom)
        else:
            assert n == len(rom)

    assert n is not None


    if n == 2:
        return LUT1(rom, **kwargs)
    if n == 4:
        return LUT2(rom, **kwargs)
    if n == 8:
        return LUT3(rom, **kwargs)
    if n == 16:
        return LUT4(rom, **kwargs)
    if n == 32:
        return LUT5(rom, **kwargs)
    if n == 64:
        return LUT6(rom, **kwargs)
    if n == 128:
        return LUT7(rom, **kwargs)
    if n == 256:
        return LUT8(rom, **kwargs)

    return None

LUT = LUTN



def Mux2(**kwargs):
    """Construct a Mux with 2 1-bit inputs."""
    MUX2DATA = (~A2&A0)|(A2&A1)
    lut = LUT3(MUX2DATA, **kwargs)
    return AnonymousCircuit("I0", lut.I0,
                            "I1", lut.I1,
                            "S", lut.I2,
                            "O", lut.O)

