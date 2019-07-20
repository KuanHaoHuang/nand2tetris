// push constant 111
@111
D=A
@R0
A=M
M=D
@R0
M=M+1
// push constant 333
@333
D=A
@R0
A=M
M=D
@R0
M=M+1
// push constant 888
@888
D=A
@R0
A=M
M=D
@R0
M=M+1
// pop static 8
@R0
M=M-1
A=M
D=M
@StaticTest.8
M=D
// pop static 3
@R0
M=M-1
A=M
D=M
@StaticTest.3
M=D
// pop static 1
@R0
M=M-1
A=M
D=M
@StaticTest.1
M=D
// push static 3
@StaticTest.3
D=M
@R0
A=M
M=D
@R0
M=M+1
// push static 1
@StaticTest.1
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
// push static 8
@StaticTest.8
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
