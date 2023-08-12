import magma as m
from .PLB import DFF
from .LUT import LUT2, A0, A1


def TFF(has_ce=False, has_reset=False, edge=True, sync=True, **kwargs):

    """A T flip-flop."""

    tff = DFF(has_ce=has_ce, has_reset=has_reset, edge=edge, sync=sync, **kwargs)
    lut = LUT2( A0^A1, **kwargs )

    lut.I0 @= tff(lut)

    args = ["I", lut.I1, "O", tff.O, "CLK", tff.CLK]
    if has_ce:    args += ['CE', dff.CE]
    if has_reset: args += ['RESET', dff.R]
    #if has_set:   args += ['SET', dff.S]

    return m.AnonymousCircuit(*args)

