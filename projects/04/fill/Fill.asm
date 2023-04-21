// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@i
M=0

@SCREEN
D=A

@addr
M=D

@fill
M=0

@filled
M=0

(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JGT

    @fill
    M=0

    @filled
    D=M
    @SETUP
    D;JGT

    @LOOP
    0;JMP

(PRESSED)
    @filled
    D=M
    @LOOP
    D;JGT

    @fill
    M=-1

    @SETUP
    0;JMP

(SETUP)
    @filled
    M=0

    @SCREEN
    D=A
    @addr
    M=D

    @256
    D=A
    @remainderCol
    M=D

(PAINTCOL)
    @32
    D=A
    @remainderRow
    M=D

    @remainderCol
    D=M
    @DONE
    D;JEQ

    @PAINTROW
    0;JMP
    
(PAINTROW)
    @remainderRow
    D=M
    @ROWDONE
    D;JEQ

    @fill
    D=M

    @addr
    A=M
    M=D
    
    @addr
    M=M+1

    @remainderRow
    M=M-1
    
    @PAINTROW
    0;JMP

(ROWDONE)
    @remainderCol
    M=M-1
    @PAINTCOL
    0;JMP

(DONE)
    @KBD
    D=M
    @LOOP
    D;JEQ

    @filled
    M=1

    @LOOP
    0;JMP