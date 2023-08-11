from magma import Circuit, DefineCircuit, EndCircuit, IO, In, Out, Bit, wire
from magma.backend.verilog import compile
from magma.testing import check_files_equal
from mantle.verilog import gates

#def test_args():
#    class Main(Circuit):
#        a = gates.And(2, name='a')
#        assert repr(a) == 'a = and(name="a")'
#        assert repr(a[0]) == 'a[0]'
#        assert repr(a[1]) == 'a[1]'
#        assert repr(a[2]) == 'a[2]'

#def test_wire():
#    class Main(Circuit):
#        a = gates.And(2, name='a')
#        wire(a[0], a[1])
#        wire(a[0], a[2])

def test_and2():
    And2 = gates.And(2)
    class Main(Circuit):
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))
        inst0 = And2()
        wire(io.I0, inst0.I0)
        wire(io.I1, inst0.I1)
        wire(inst0.O, io.O)

    print(repr(Main))
    assert repr(Main) == '''\
Main = DefineCircuit("Main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
And2_inst0 = And2()
wire(Main.I0, And2_inst0.I0)
wire(Main.I1, And2_inst0.I1)
wire(And2_inst0.O, Main.O)
EndCircuit()'''


    print(compile(Main))
    assert compile(Main) == '''\
module Main (input  I0, input  I1, output  O);
wire  And2_inst0_O;
And2 And2_inst0 (.O(And2_inst0_O), .I0(I0), .I1(I1));
assign O = And2_inst0_O;
endmodule

'''

def test_nand2():
    NAnd2 = DefineCircuit("NAnd2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    inst0 = gates.NAnd(2)
    wire(NAnd2.I0, inst0[1])
    wire(NAnd2.I1, inst0[2])
    wire(inst0[0], NAnd2.O)
    EndCircuit()

    assert repr(NAnd2) == '''\
NAnd2 = DefineCircuit("NAnd2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
nand_inst0 = nand()
wire(NAnd2.I0, nand_inst0[1])
wire(NAnd2.I1, nand_inst0[2])
wire(nand_inst0[0], NAnd2.O)
EndCircuit()'''

    assert compile(NAnd2) == '''\
module NAnd2 (input  I0, input  I1, output  O);
wire  nand_inst0_0;
nand nand_inst0 (nand_inst0_0, I0, I1);
assign O = nand_inst0_0;
endmodule

'''

def test_or2():
    or2 = DefineCircuit("or2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    inst0 = gates.Or(2)
    wire(or2.I0, inst0[1])
    wire(or2.I1, inst0[2])
    wire(inst0[0], or2.O)
    EndCircuit()

    assert repr(or2) == '''\
or2 = DefineCircuit("or2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
or_inst0 = or()
wire(or2.I0, or_inst0[1])
wire(or2.I1, or_inst0[2])
wire(or_inst0[0], or2.O)
EndCircuit()'''

    assert compile(or2) == '''\
module or2 (input  I0, input  I1, output  O);
wire  or_inst0_0;
or or_inst0 (or_inst0_0, I0, I1);
assign O = or_inst0_0;
endmodule

'''

def test_nor2():
    nor2 = DefineCircuit("nor2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    inst0 = gates.NOr(2)
    wire(nor2.I0, inst0[1])
    wire(nor2.I1, inst0[2])
    wire(inst0[0], nor2.O)
    EndCircuit()

    assert repr(nor2) == '''\
nor2 = DefineCircuit("nor2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
nor_inst0 = nor()
wire(nor2.I0, nor_inst0[1])
wire(nor2.I1, nor_inst0[2])
wire(nor_inst0[0], nor2.O)
EndCircuit()'''

    assert compile(nor2) == '''\
module nor2 (input  I0, input  I1, output  O);
wire  nor_inst0_0;
nor nor_inst0 (nor_inst0_0, I0, I1);
assign O = nor_inst0_0;
endmodule

'''

def test_xor2():
    xor2 = DefineCircuit("xor2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    inst0 = gates.XOr(2)
    wire(xor2.I0, inst0[1])
    wire(xor2.I1, inst0[2])
    wire(inst0[0], xor2.O)
    EndCircuit()

    assert repr(xor2) == '''\
xor2 = DefineCircuit("xor2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
xor_inst0 = xor()
wire(xor2.I0, xor_inst0[1])
wire(xor2.I1, xor_inst0[2])
wire(xor_inst0[0], xor2.O)
EndCircuit()'''

    assert compile(xor2) == '''\
module xor2 (input  I0, input  I1, output  O);
wire  xor_inst0_0;
xor xor_inst0 (xor_inst0_0, I0, I1);
assign O = xor_inst0_0;
endmodule

'''

def test_nxor2():
    nxor2 = DefineCircuit("nxor2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    inst0 = gates.NXOr(2)
    wire(nxor2.I0, inst0[1])
    wire(nxor2.I1, inst0[2])
    wire(inst0[0], nxor2.O)
    EndCircuit()

    assert repr(nxor2) == '''\
nxor2 = DefineCircuit("nxor2", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
nxor_inst0 = nxor()
wire(nxor2.I0, nxor_inst0[1])
wire(nxor2.I1, nxor_inst0[2])
wire(nxor_inst0[0], nxor2.O)
EndCircuit()'''

    assert compile(nxor2) == '''\
module nxor2 (input  I0, input  I1, output  O);
wire  nxor_inst0_0;
nxor nxor_inst0 (nxor_inst0_0, I0, I1);
assign O = nxor_inst0_0;
endmodule

'''

def test_not():
    n = DefineCircuit("n", "I", In(Bit), "O", Out(Bit))
    inst0 = gates.Not()
    inst0.I @= n.I
    n.O @= inst0.O
    EndCircuit()

    assert repr(n) == '''\
n = DefineCircuit("n", "I", In(Bit), "O", Out(Bit))
not_inst0 = not()
wire(n.I, not_inst0[1])
wire(not_inst0[0], n.O)
EndCircuit()'''

    assert compile(n) == '''\
module n (input  I, output  O);
wire  not_inst0_0;
not not_inst0 (not_inst0_0, I);
assign O = not_inst0_0;
endmodule

'''
