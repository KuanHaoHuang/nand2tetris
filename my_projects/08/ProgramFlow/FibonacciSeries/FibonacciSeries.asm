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
// pop pointer 1
@R0
M=M-1
A=M
D=M
@R4
M=D
// push constant 0
@0
D=A
@R0
A=M
M=D
@R0
M=M+1
// pop that 0
@R0
M=M-1
@R4
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
// push constant 1
@1
D=A
@R0
A=M
M=D
@R0
M=M+1
// pop that 1
@R0
M=M-1
@R4
D=M
@1
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
// labeling: MAIN_LOOP_START
(MAIN_LOOP_START)
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
// if-goto: COMPUTE_ELEMENT
@R0
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JNE
// goto: END_PROGRAM
@END_PROGRAM
0;JMP
// labeling: COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
// push that 0
@R4
D=M
@0
A=D+A
D=M
@R0
A=M
M=D
@R0
M=M+1
// push that 1
@R4
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
// pop that 2
@R0
M=M-1
@R4
D=M
@2
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
// push pointer 1
@R4
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
// pop pointer 1
@R0
M=M-1
A=M
D=M
@R4
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
// goto: MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP
// labeling: END_PROGRAM
(END_PROGRAM)
