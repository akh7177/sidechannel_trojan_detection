`timescale 1ns/1ps
module tb_single;
    reg [3:0] A;
    reg [3:0] B;
    reg [1:0] op;
    integer i, j, k;

    wire [3:0] Y;
    wire carry_out, zero_flag;
    alu alu_instance (.A(A), .B(B), .op(op), .Y(Y), .carry_out(carry_out), .zero_flag(zero_flag));

    initial begin
        $dumpfile(`DUMPFILE);  
        $dumpvars(0, tb_single.alu_instance);
    end

    initial begin
        A = 0; B = 0; op = 0;
        #1;
        for (i = 0; i < 16; i = i + 1)
            for (j = 0; j < 16; j = j + 1)
                for (k = 0; k < 4; k = k + 1) begin
                    A = i; B = j; op = k; #1;
                end
        #5; $finish;
    end
endmodule
