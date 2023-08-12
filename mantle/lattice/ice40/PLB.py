import hwtypes as ht

from magma.bit import Bit
from magma.circuit import Circuit
from magma.clock import Clock, Reset, Enable
from magma.interface import IO
from magma.t import In, Out


# Useful variables for programming LUTs
LUTS_PER_LOGICBLOCK = 2
LOG_BITS_PER_LUT = 4
BITS_PER_LUT = 1 << LOG_BITS_PER_LUT

ZERO = 0
ONE = (1 << BITS_PER_LUT) - 1

A0 = ht.BitVector[16](0xAAAA)
A1 = ht.BitVector[16](0xCCCC)
A2 = ht.BitVector[16](0xF0F0)
A3 = ht.BitVector[16](0xFF00)

I0 = A0
I1 = A1
I2 = A2
I3 = A3

ALL = A0 & A1 & A2 & A3
ANY = A0 | A1 | A2 | A3
PARITY = A0 ^ A1 ^ A2 ^ A3


class SB_LUT4(Circuit):
    io = IO(
        I0=In(Bit),
        I1=In(Bit),
        I2=In(Bit),
        I3=In(Bit),
        O=Out(Bit)
    )
    param_types = {"LUT_INIT": ht.BitVector[16]}


class SB_CARRY(Circuit):
    """Implements (I0&I1)|(I1&I2)|(I2&I0)"""
    io = IO(
        I0=In(Bit),  # must be the same as SB_LUT4 I1 to pack
        I1=In(Bit),  # must be the same as SB_LUT4 I2 to pack
        CI=In(Bit),  # must be from previous SB_LUT4 to pack
        CO=Out(Bit)
    )


class SB_DFF(Circuit):
    io = IO(
        C=In(Clock),
        D=In(Bit),
        Q=Out(Bit)
    )

# Positive edge versions

# DFF - D Flip-Flop
class SB_DFF(Circuit):
    """D Flip-Flop"""
    io = IO(
        C=In(Clock),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=False, r=False, s=False, n=False),
    #coreir_lib="ice40")

class SB_DFFE(Circuit):
    """DFF w/ Clock enable"""
    io = IO(
        C=In(Clock),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=False, r=False, s=False, n=False),
    #coreir_lib="ice40"

class SB_DFFSR(Circuit):
    '''DFF w/ Synchronous Reset'''
    io = IO(
        C=In(Clock),
        R=In(Reset),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=True, r=True, s=False, n=False),
    #coreir_lib="ice40"

class SB_DFFR(Circuit):
    '''DFF w/ Asynchronous Reset'''
    io = IO(
        C=In(Clock),
        R=In(Reset),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=False, r=True, s=False, n=False),
    #coreir_lib="ice40"

# DFF w/ Synchronous Set
class SB_DFFSS(Circuit):
    io = IO(
        C=In(Clock),
        S=In(Bit),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=True, r=False, s=True, n=False),
    #coreir_lib="ice40"

class SB_DFFS(Circuit):
    '''DFF w/ Asynchronous Set'''
    io = IO(
        C=In(Clock),
        S=In(Bit),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=False, r=False, s=True, n=False),
    #coreir_lib="ice40"

class SB_DFFESR(Circuit):
    '''DFF w/ Synchronous Reset, Clock enable'''
    io = IO(
        C=In(Clock),
        R=In(Reset),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=True, r=True, s=False, n=False),
    #coreir_lib="ice40"

class SB_DFFER(Circuit):
    '''DFF w/ Asynchronous Reset, Clock enable'''
    io = IO(
        C=In(Clock),
        R=In(Reset),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=False, r=True, s=False, n=False),
    #coreir_lib="ice40"

class SB_DFFESS(Circuit):
    '''DFF w/ Synchronous Set, Clock enable'''
    io = IO(
        C=In(Clock),
        S=In(Bit),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=True, r=False, s=True, n=False),
    #coreir_lib="ice40"

class SB_DFFES(Circuit):
    '''DFF w/ Asynchronous Set, Clock enable'''
    io = IO(
        C=In(Clock),
        S=In(Bit),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=False, r=False, s=True, n=False),
    #coreir_lib="ice40"

# Negative edge versions

class SB_DFFN(Circuit):
    io = IO(
        C=In(Clock),
        D=In(Bit),
        Q=Out(Bit)
    )

# Positive edge versions

# DFF - D Flip-Flop
class SB_DFFN(Circuit):
    """D Flip-Flop"""
    io = IO(
        C=In(Clock),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=False, r=False, s=False, n=False),
    #coreir_lib="ice40")

class SB_DFFNE(Circuit):
    """DFF w/ Clock enable"""
    io = IO(
        C=In(Clock),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=False, r=False, s=False, n=False),
    #coreir_lib="ice40"

class SB_DFFNSR(Circuit):
    '''DFF w/ Synchronous Reset'''
    io = IO(
        C=In(Clock),
        R=In(Reset),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=True, r=True, s=False, n=False),
    #coreir_lib="ice40"

class SB_DFFNR(Circuit):
    '''DFF w/ Asynchronous Reset'''
    io = IO(
        C=In(Clock),
        R=In(Reset),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=False, r=True, s=False, n=False),
    #coreir_lib="ice40"

# DFF w/ Synchronous Set
class SB_DFFNSS(Circuit):
    io = IO(
        C=In(Clock),
        S=In(Bit),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=True, r=False, s=True, n=False),
    #coreir_lib="ice40"

class SB_DFFNS(Circuit):
    '''DFF w/ Asynchronous Set'''
    io = IO(
        C=In(Clock),
        S=In(Bit),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=False, sy=False, r=False, s=True, n=False),
    #coreir_lib="ice40"

class SB_DFFNESR(Circuit):
    '''DFF w/ Synchronous Reset, Clock enable'''
    io = IO(
        C=In(Clock),
        R=In(Reset),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=True, r=True, s=False, n=False),
    #coreir_lib="ice40"

class SB_DFFNER(Circuit):
    '''DFF w/ Asynchronous Reset, Clock enable'''
    io = IO(
        C=In(Clock),
        R=In(Reset),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=False, r=True, s=False, n=False),
    #coreir_lib="ice40"

class SB_DFFNESS(Circuit):
    '''DFF w/ Synchronous Set, Clock enable'''
    io = IO(
        C=In(Clock),
        S=In(Bit),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=True, r=False, s=True, n=False),
    #coreir_lib="ice40"

class SB_DFFNES(Circuit):
    '''DFF w/ Asynchronous Set, Clock enable'''
    io = IO(
        C=In(Clock),
        S=In(Bit),
        E=In(Enable),
        D=In(Bit),
        Q=Out(Bit)
    )
    #stateful=True,
    #simulate=gen_sb_dff_sim(ce=True, sy=False, r=False, s=True, n=False),
    #coreir_lib="ice40"
