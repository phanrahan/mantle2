import magma as m
from .PLB import *
from .LUT import LUT1, LUT2, LUT3, A0


def _DFF(has_ce=False, has_reset=False, edge=True, sync=True):
    # has_set not supported
    has_set = False

    # By default
    #  not connecting a wire to D defaults to 0
    #  not connecting a wire to C defaults to 0
    #  not connecting a wire to R defaults to 0
    #  not connecting a wire to E defaults to 1
    #   this is better than connecting a 1 to E,
    #   which causes that signal to be generated
    if edge:
        # rising edge
        if sync:
            # synchronous reset
            if has_ce:
                if   has_reset:
                    return SB_DFFESR
                elif has_set:
                    return SB_DFFESS
                else:
                    return SB_DFFE
            else:
                if   has_reset:
                    return SB_DFFSR
                elif has_set:
                    return SB_DFFSS
                else:
                    return SB_DFF
        else:
            # asynchronous reset
            if has_ce:
                if   has_reset:
                    return SB_DFFER
                elif has_s:
                    return SB_DFFES
                else:
                    return SB_DFFE
            else:
                if   has_reset:
                    return SB_DFFR
                elif has_set:
                    return SB_DFFS
                else:
                    return SB_DFF
    else:
        # falling edge
        if sync:
            # synchronous reset
            if has_ce:
                if   has_reset:
                    return SB_DFFNESR
                elif has_set:
                    return SB_DFFNESS
                else:
                    return SB_DFFNE
            else:
                if   has_reset:
                    return SB_DFFNSR
                elif has_set:
                    return SB_DFFNSS
                else:
                    return SB_DFFN
        else:
            # asynchronous reset
            if has_ce:
                if   has_reset:
                    return SB_DFFNER
                elif has_set:
                    return SB_DFFNES
                else:
                    return SB_DFFNE
            else:
                if   has_reset:
                    return SB_DFFNR
                elif has_set:
                    return SB_DFFNS
                else:
                    return SB_DFFN

def _Not():
    """Not gate - 1-bit input."""
    return LUT1(~A0)

#
# TODO: add async=True, edge=True (also negedge)
#
def DFF(init=0, has_ce=False, has_reset=False, edge=True, sync=True, **kwargs):

    ff = _DFF(has_ce, has_reset, edge, sync)(**kwargs)

    I = ff.D
    O = ff.Q

    # ice40 flip-flops are initialized to 0 by default
    #  this code emulates initializing them to 1
    if init:
        # if init=1, then insert Not before and after the flip-flop
        luti = _Not()
        luto = _Not()
        ff.D @= luti.O
        luto.I0 @= ff.Q
        I = luti.I0
        O = luto.O

    args = ['I', I, 'CLK', ff.C]
    if has_ce:
        args += ['CE', ff.E]
    if has_reset:
        args += ['RESET', ff.R]
    #if has_set:
    #    args += ['SET', ff.S]

    args += ['O', O]

    return m.AnonymousCircuit(args)

FF = DFF
