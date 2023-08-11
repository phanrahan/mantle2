import magma as m

__all__ = ['Buf']

def Buf(m.Generator2):
    """
    Generate Buf module

    I : In(Bits(width)), O : Out(Bits(width))
    """
    def __init__(self, width: int):
        T = m.Bits[width]
        self.io  = ['I', m.In(T), 'O', m.Out(T)]

        def buf(y):
            return Buf(loc=(0,y//8, y%8))
        buffer = join(col(buf, width))
        buffer.I @= io.I
        io.O @= buffer.O


