// Bootstrap
@256
D=A
@R0
M=D
// call function: Sys.init, #args=0
@RET$0
D=A
@R15
M=D
@R15
D=M
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@R3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@5
D=A
@0
D=D+A
@R0
D=M-D
@R2
M=D
@R0
D=M
@R1
M=D
@Sys.init
0;JMP
(RET$0)
// def function: Main.fibonacci, #vars=0
(Main.fibonacci)
// push argument 0
@R2
D=M
@0
A=D+A
D=M
@R0
A=M
M=D
@R0
M=M+1
// push constant 2
@2
D=A
@R0
A=M
M=D
@R0
M=M+1
// lt
@R0
M=M-1
A=M
D=-M
@R0
M=M-1
A=M
D=D+M
M=-1
@IF_LT_1_
D;JLT
@R0
A=M
M=0
(IF_LT_1_)
@R0
M=M+1
// if-goto: IF_TRUE
@R0
M=M-1
A=M
D=M
@IF_TRUE
D;JNE
// goto: IF_FALSE
@IF_FALSE
0;JMP
// labeling: IF_TRUE
(IF_TRUE)
// push argument 0
@R2
D=M
@0
A=D+A
D=M
@R0
A=M
M=D
@R0
M=M+1
// return
@R1
D=M
@R13
M=D
@5
A=D-A
D=M
@R15
M=D
@R0
M=M-1
A=M
D=M
@R2
A=M
M=D
@R2
D=M+1
@R0
M=D
@R13
D=M
D=D-1
A=D
D=M
@4
M=D
@R13
D=M
D=D-1
D=D-1
A=D
D=M
@3
M=D
@R13
D=M
D=D-1
D=D-1
D=D-1
A=D
D=M
@2
M=D
@R13
D=M
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@1
M=D
@R15
A=M
0;JMP
// labeling: IF_FALSE
(IF_FALSE)
// push argument 0
@R2
D=M
@0
A=D+A
D=M
@R0
A=M
M=D
@R0
M=M+1
// push constant 2
@2
D=A
@R0
A=M
M=D
@R0
M=M+1
// sub
@R0
M=M-1
A=M
D=-M
@R0
M=M-1
A=M
M=D+M
@R0
M=M+1
// call function: Main.fibonacci, #args=1
@RET$2
D=A
@R15
M=D
@R15
D=M
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@R3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@5
D=A
@1
D=D+A
@R0
D=M-D
@R2
M=D
@R0
D=M
@R1
M=D
@Main.fibonacci
0;JMP
(RET$2)
// push argument 0
@R2
D=M
@0
A=D+A
D=M
@R0
A=M
M=D
@R0
M=M+1
// push constant 1
@1
D=A
@R0
A=M
M=D
@R0
M=M+1
// sub
@R0
M=M-1
A=M
D=-M
@R0
M=M-1
A=M
M=D+M
@R0
M=M+1
// call function: Main.fibonacci, #args=1
@RET$3
D=A
@R15
M=D
@R15
D=M
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@R3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@5
D=A
@1
D=D+A
@R0
D=M-D
@R2
M=D
@R0
D=M
@R1
M=D
@Main.fibonacci
0;JMP
(RET$3)
// add
@R0
M=M-1
A=M
D=M
@R0
M=M-1
A=M
M=D+M
@R0
M=M+1
// return
@R1
D=M
@R13
M=D
@5
A=D-A
D=M
@R15
M=D
@R0
M=M-1
A=M
D=M
@R2
A=M
M=D
@R2
D=M+1
@R0
M=D
@R13
D=M
D=D-1
A=D
D=M
@4
M=D
@R13
D=M
D=D-1
D=D-1
A=D
D=M
@3
M=D
@R13
D=M
D=D-1
D=D-1
D=D-1
A=D
D=M
@2
M=D
@R13
D=M
D=D-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@1
M=D
@R15
A=M
0;JMP
// def function: Sys.init, #vars=0
(Sys.init)
// push constant 4
@4
D=A
@R0
A=M
M=D
@R0
M=M+1
// call function: Main.fibonacci, #args=1
@RET$4
D=A
@R15
M=D
@R15
D=M
@R0
A=M
M=D
@R0
M=M+1
@R1
D=M
@R0
A=M
M=D
@R0
M=M+1
@R2
D=M
@R0
A=M
M=D
@R0
M=M+1
@R3
D=M
@R0
A=M
M=D
@R0
M=M+1
@R4
D=M
@R0
A=M
M=D
@R0
M=M+1
@5
D=A
@1
D=D+A
@R0
D=M-D
@R2
M=D
@R0
D=M
@R1
M=D
@Main.fibonacci
0;JMP
(RET$4)
// labeling: WHILE
(WHILE)
// goto: WHILE
@WHILE
0;JMP