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

(LOOP)

   @KBD
   D=M
   @END
   D;JEQ
   
   @R0
   D=A
   @i
   M=D
   @SCREEN
   D=A
   @scr
   M=D
   (INLOOP)
   @8191
   D=A
   @i
   D=M-D
   @INEND
   D;JGT
   
   @scr
   A=M
   M=-1
   
   @scr
   M=M+1
   @i
   M=M+1
   @INLOOP
   0;JMP

(END)
   @R0
   D=A
   @i
   M=D
   @SCREEN
   D=A
   @scr
   M=D
   (CLEANLOOP)
   @8191
   D=A
   @i
   D=M-D
   @INEND
   D;JGT
   
   @scr
   A=M
   M=0
   
   @scr
   M=M+1
   @i
   M=M+1
   @CLEANLOOP
   0;JMP

(INEND)
   @LOOP
   0;JMP
