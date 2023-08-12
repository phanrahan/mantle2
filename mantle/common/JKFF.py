import magma as m
from .FF import DFF
from .LUT import LUT3, A0, A1, A2


def JKFF(has_ce=False, has_reset=False, edge=True, sync=True, **kwargs):

    """A J-K flip-flop."""

    dff = DFF(has_ce=has_ce, has_reset=has_reset, edge=edge, sync=sync, **kwargs)
    lut = LUT3( (~A0&A1)|(A0&~A2), **kwargs )

    lut.I0 @= dff(lut)

    args = ["J", lut.I1, "K", lut.I2, "O", dff.O, 'CLK', dff.CLK]
    if has_ce:     args += ['CE', dff.CE]
    if has_reset:  args += ['RESET', dff.R]
    #if has_set:    args += ['SET', dff.S]

    return m.AnonymousCircuit(*args)


