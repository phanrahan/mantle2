import magma as m
from .DFF import DFF
from .LUT import LUT3, A0, A1, A2

def RSFF(init=0, has_ce=False, edge=True, sync=True, **kwargs):

    """A R-S flip-flop."""

    dff = DFF( init=init, has_ce=has_ce, edge=edge, sync=sync, **kwargs)

    lut = LUT3( (~A1&~A2&A0)|(A1&~A2), **kwargs )
    lut.I0 @= dff(lut)

    args = []
    if has_ce:
        args += ['CE', dff.CE]
    args += ["R", lut.I2, "S", lut.I1, 'CLK', dff.CLK, "O", dff.O]

    return AnonymousCircuit(args)


