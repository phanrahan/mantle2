import magma as m
from magma.backend.verilog import compile
from magma.testing import check_files_equal
from mantle.verilog import DFF

def test_dff():
    main = m.DefineCircuit('main', 'I', m.In(m.Bit), "O", m.Out(m.Bit), "CLK", m.In(m.Clock))
    dff = DFF()
    m.wire(main.I, dff.D)
    m.wire(dff.Q, main.O)
    m.EndCircuit()

    assert compile(main) == '''\
module DFF (input  D, input  CLK, output  Q);
    always @(posedge CLK) begin
        Q <= D;
    end
endmodule

module main (input  I, output  O, input  CLK);
wire  DFF_inst0_Q;
DFF DFF_inst0 (.D(I), .CLK(CLK), .Q(DFF_inst0_Q));
assign O = DFF_inst0_Q;
endmodule

'''
  
