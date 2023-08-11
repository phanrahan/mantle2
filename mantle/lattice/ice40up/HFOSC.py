import magma as m

# generate 48 Mhz clock
class SB_HFOSC(m.Circuit):
    io = m.IO(
        CLKHFPU=m.In(m.Bit), # power up
        CLKHFEN=m.In(m.Bit), # enable
        CLKHF=  m.Out(m.Clock)
    )
                         )

# parameters
#  CLKHF_DIV 0b00 48Mhz
#            0b01 24Mhz
#            0b10 12Mhz
#            0b11 6Mhz

#SB_HFOSC u_hfosc (
#                .CLKHFPU(1'b1),
#                .CLKHFEN(1'b1),
#                .CLKHF(clk)
#        );
