// push constant 0
@0
D=A
@R0
A=M
M=D
@R0
M=M+1
// pop local 0
@R0
M=M-1
@R1
D=M
@0
A=D+A
D=A
@tmp_
M=D
@R0
A=M
D=M
@tmp_
A=M
M=D
// labeling: LOOP_START
(LOOP_START)
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
// pop local 0
@R0
M=M-1
@R1
D=M
@0
A=D+A
D=A
@tmp_
M=D
@R0
A=M
D=M
@tmp_
A=M
M=D
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
// pop argument 0
@R0
M=M-1
@R2
D=M
@0
A=D+A
D=A
@tmp_
M=D
@R0
A=M
D=M
@tmp_
A=M
M=D
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
// if-goto: LOOP_START
@R0
M=M-1
A=M
D=M
@LOOP_START
D;JNE
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
