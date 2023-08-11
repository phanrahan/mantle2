import magma as m

__all__  = ['And']
__all__ += ['NAnd']
__all__ += ['Or']
__all__ += ['NOr']
__all__ += ['XOr']
__all__ += ['NXOr']
__all__ += ['Not']
__all__ += ['Buf']

def args(n=2):
    d = {"O":m.Out(m.Bit)}
    for i in range(n):
        d[f"I{i}"] = m.In(m.Bit)
    return d


class And(m.Generator2):
    def __init__(self, n=2, **kwargs):
        self.name = f"And{n}"
        self.io = m.IO(**args(n))

class NAnd(m.Generator2):
    def __init__(self, n=2, **kwargs):
        self.name = f"NAnd{n}"
        self.io = m.IO(**args(n))


class Or(m.Generator2):
    def __init__(self, n=2, **kwargs):
        self.name = f"Or{n}"
        self.io = m.IO(**args(n))

class NOr(m.Generator2):
    def __init__(self, n=2, **kwargs):
        self.name = f"NOr{n}"
        self.io = m.IO(**args(n))


class XOr(m.Generator2):
    def __init__(self, n=2, **kwargs):
        self.name = f"XOr{n}"
        self.io = m.IO(**args(n))

class NXOr(m.Generator2):
    def __init__(self, n=2, **kwargs):
        self.name = f"NXOr{n}"
        self.io = m.IO(**args(n))


class Not(m.Generator2):
    def __init__(self, **kwargs):
        self.io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))


class Buf(m.Generator2):
    def __init__(self, **kwargs):
        self.io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
