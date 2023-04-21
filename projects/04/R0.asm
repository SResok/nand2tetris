// if R0>0
//    R1=1
// else
//    R1=0

@R0
D=M

@8    //jump to make 1
D;JGT

@R1
M=0

@10
0;JMP

@R1 // jump here
M=1

@10
0;JMP

