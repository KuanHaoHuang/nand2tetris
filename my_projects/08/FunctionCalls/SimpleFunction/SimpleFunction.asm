// def function: SimpleFunction.test, #vars=2
(SimpleFunction.test)
@0
D=A
@R0
A=M
M=D
@R0
M=M+1
@0
D=A
@R0
A=M
M=D
@R0
M=M+1
// push local 0
@R1
D=M
@0
A=D+A
D=M
@R0
A=M
M=D
@R0
M=M+1
// push local 1
@R1
D=M
@1
A=D+A
D=M
@R0
A=M
M=D
@R0
M=M+1
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
// not
@R0
M=M-1
A=M
M=!M
@R0
M=M+1
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
// push argument 1
@R2
D=M
@1
A=D+A
D=M
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
