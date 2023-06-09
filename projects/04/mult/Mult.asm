// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

@sum
M=0

@R1
D=M

@STOP // stop if R1 = <= 0
D;JLE

@R0
D=M

@STOP // stop if R0 = <= 0
D;JLE

@remainder // remainder = R0
M=D

(LOOP)

    @remainder
    D=M

    @STOP // stop if remainder 0
    D;JEQ

    // SUM + R1
    @R1
    D=M

    @sum
    M=M+D

    // remainder --
    @remainder
    M=M-1

    @LOOP
    0;JMP


(STOP) // set sum to R2
    @sum
    D=M

    @R2
    M=D

(END)
    @END
    0;JMP
    

    