import magma as m

class SB_IO(m.Circuit):
    io = m.IO(
        PACKAGE_PIN=m.In(m.Bit), # should be inout
        CLOCK_ENABLE=m.In(m.Bit),
        INPUT_CLOCK=m.In(m.Bit),
        OUTPUT_CLOCK=m.In(m.Bit),
        OUTPUT_ENABLE=m.In(m.Bit),
        LATCH_INPUT_VALUE=m.In(m.Bit),
        D_IN_0=m.In(m.Bit),       # rising
        D_IN_1=m.In(m.Bit),       # falling
        D_OUT_0=m.Out(m.Bit),     # rising
        D_OUT_1=m.Out(m.Bit)      # falling
     )

#module top (input PIO1_02, output D1);
#wire y;
#SB_IO #(.PIN_TYPE(6'b00_0000)) in  ( .PACKAGE_PIN(PIO1_02), .D_IN_0(y) );
#SB_IO #(.PIN_TYPE(6'b01_0110)) out ( .PACKAGE_PIN(D1), .D_OUT_0(y) );
#endmodule

