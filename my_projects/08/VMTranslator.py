#!/usr/bin/python3
import os
import sys

class Parser:
    def __init__(self, file_path):
        with open(file_path, "r") as f:
            self.file = f.readlines()
        self.current_command = None
        self.index = -1

    def hasMoreCommands(self):
        return (self.index + 1) in range(len(self.file))

    def advance(self):
        # use this function only if hasMoreCommands
        line = self.file[self.index+1].strip()
        while (len(line) == 0 or line[0] == "/"):
            self.file.pop(self.index + 1)
            line = self.file[self.index+1].strip()
        if line.find("/") >= 0:
            self.current_command = line[0:line.find("/")].strip()
        else:
            self.current_command = line.strip()
        self.index = self.index + 1
        return

    def commandType(self):
        assert self.current_command is not None and len(
            self.current_command) > 0
        t = self.current_command.split()[0]
        if t in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return "C_ARITHMETIC"
        elif t == "push":
            return "C_PUSH"
        elif t == "pop":
            return "C_POP"
        elif t == "label":
            return "C_LABEL"
        elif t == "if-goto":
            return "C_IF"
        elif t == "goto":
            return "C_GOTO"
        elif t == "function":
            return "C_FUNCTION"
        elif t == "return":
            return "C_RETURN"
        elif t == "call":
            return "C_CALL"
        else:
            return "unknown"

    def arg1(self):
        assert self.current_command is not None \
            and len(self.current_command) > 0
        if self.commandType() == "C_ARITHMETIC":
            return self.current_command.split()[0]
        else:
            return self.current_command.split()[1]

    def arg2(self):
        assert self.current_command is not None \
            and len(self.current_command) > 0 \
            and len(self.current_command.split()) > 2 \
            and self.commandType() in ("C_PUSH", "C_POP", "C_FUNCTION", "C_CALL")
        return self.current_command.split()[2]

class CodeWriter:
    def __init__(self, file_path):
        with open(file_path, 'w') as f:
            f.write("")
        self.file = open(file_path, "a")
        self.file_id = file_path.split("/")[-1].split(".")[0]
        self._jmp_counter = 0
        self.vm_title = ""

    def setVMTitle(self, title):
        # mainly used for Statics
        self.vm_title = title

    def close(self):
        self.file.close()

    def writeInit(self):
        f = self.file
        f.write("// " + "Bootstrap" + "\n")
        # SP = 256
        f.write("@256" + "\n")
        f.write("D=A" + "\n")
        f.write("@R0" + "\n")
        f.write("M=D" + "\n")
        # call Sys.init 0
        self.writeCall("Sys.init")
    
    def writeLabel(self, label):
        f = self.file
        f.write("// " + "labeling: " + label + "\n")
        f.write("(" + label + ")" + "\n")

    def writeGoto(self, label):
        f = self.file
        f.write("// " + "goto: " + label + "\n")
        f.write("@" + label + "\n")
        f.write("0;JMP" + "\n")
        
    def writeIf(self, label):
        f = self.file
        f.write("// " + "if-goto: " + label + "\n")
        f.write("@R0" + "\n")
        f.write("M=M-1" + "\n")
        f.write("A=M" + "\n")
        f.write("D=M" + "\n")
        f.write("@" + label + "\n")
        f.write("D;JNE" + "\n")
 
    def writeFunction(self, functionName, numVars = 0):
        numVars = int(numVars)
        f = self.file
        f.write("// " + "def function: " + functionName + ", #vars=" + str(numVars) + "\n")
        f.write("(" + functionName + ")" + "\n")
        # repeat nVars times: push 0
        for _ in range(numVars):
            f.write("@0" + "\n")
            f.write("D=A" + "\n")
            f.write("@R0" + "\n") # push D to SP starts
            f.write("A=M" + "\n")
            f.write("M=D" + "\n")
            f.write("@R0" + "\n")
            f.write("M=M+1" + "\n") # push D to SP ends
        
    def writeCall(self, functionName, numArgs = 0):
        numArgs = int(numArgs)
        f = self.file
        f.write("// " + "call function: " + functionName + ", #args=" + str(numArgs) + "\n")
        f.write("@RET$" + str(self._jmp_counter) + "\n")
        f.write("D=A" + "\n")
        f.write("@R15" + "\n")
        f.write("M=D" + "\n")
        for r in ["R15", "R1", "R2", "R3", "R4"]:
            f.write("@" + r + "\n")
            f.write("D=M" + "\n")
            f.write("@R0" + "\n") # push D to SP starts
            f.write("A=M" + "\n")
            f.write("M=D" + "\n")
            f.write("@R0" + "\n")
            f.write("M=M+1" + "\n") # push D to SP ends
        # ARG = SP-5-nArgs
        f.write("@5" + "\n")
        f.write("D=A" + "\n")
        f.write("@" + str(numArgs) + "\n")
        f.write("D=D+A" + "\n")
        f.write("@R0" + "\n")
        f.write("D=M-D" + "\n")
        f.write("@R2" + "\n")
        f.write("M=D" + "\n")
        # LCL = SP
        f.write("@R0" + "\n")
        f.write("D=M" + "\n")
        f.write("@R1" + "\n")
        f.write("M=D" + "\n")
        # goto functionName
        f.write("@" + functionName + "\n")
        f.write("0;JMP" + "\n")
        f.write("(" + "RET$" + str(self._jmp_counter) + ")" + "\n")
        self._jmp_counter += 1

    def writeReturn(self):
        f = self.file
        f.write("// " + "return" + "\n")
        # endFrame = LCL
        f.write("@R1" + "\n")
        f.write("D=M" + "\n")
        f.write("@R13" + "\n")
        f.write("M=D" + "\n")
        # retAddr = *(endFrame – 5) 
        f.write("@5" + "\n")
        f.write("A=D-A" + "\n")
        f.write("D=M" + "\n")
        f.write("@R15" + "\n")
        f.write("M=D" + "\n")
        # *ARG=pop()
        f.write("@R0" + "\n")
        f.write("M=M-1" + "\n")
        f.write("A=M" + "\n")
        f.write("D=M" + "\n")
        f.write("@R2" + "\n")
        f.write("A=M" + "\n")
        f.write("M=D" + "\n")
        # SP = ARG + 1
        f.write("@R2" + "\n")
        f.write("D=M+1" + "\n")
        f.write("@R0" + "\n")
        f.write("M=D" + "\n")
        # restores THAT, THIS, ARG, LCL
        for i in [1, 2, 3, 4]:
            f.write("@R13" + "\n")
            f.write("D=M" + "\n")
            for j in range(i):
                f.write("D=D-1" + "\n")
            f.write("A=D" + "\n")
            f.write("D=M" + "\n")
            f.write("@" + str(5-i) + "\n")
            f.write("M=D" + "\n")
        # goto retAddr
        f.write("@R15" + "\n")
        f.write("A=M" + "\n")
        f.write("0;JMP" + "\n")

    # f.write("" + "\n")
    def writeArithmetic(self, command):
        f = self.file
        f.write("// " + command + "\n")
        f.write("@R0" + "\n")
        f.write("M=M-1" + "\n")
        f.write("A=M" + "\n")
        # f.write("D=M" + "\n")
        if command == "add" or command == "sub":
            if command == "add":
                f.write("D=M" + "\n")
            else:
                f.write("D=-M" + "\n")
            f.write("@R0" + "\n")
            f.write("M=M-1" + "\n")
            f.write("A=M" + "\n")
            f.write("M=D+M" + "\n")
        elif command == "neg":
            f.write("M=-M" + "\n")
        elif command == "not":
            f.write("M=!M" + "\n")
        elif command in ["eq", "gt", "lt"]:
            f.write("D=-M" + "\n")
            f.write("@R0" + "\n")
            f.write("M=M-1" + "\n")
            f.write("A=M" + "\n")
            f.write("D=D+M" + "\n")
            f.write("M=-1" + "\n")
            if command == "eq":
                f.write("@IF_EQ_" + str(self._jmp_counter) + "_" + "\n")
                f.write("D;JEQ" + "\n")
                f.write("@R0" + "\n")
                f.write("A=M" + "\n")
                f.write("M=0" + "\n")
                f.write("(IF_EQ_" + str(self._jmp_counter) + "_)" + "\n")
                self._jmp_counter += 1
            elif command == "gt":
                f.write("@IF_GT_" + str(self._jmp_counter) + "_" + "\n")
                f.write("D;JGT" + "\n")
                f.write("@R0" + "\n")
                f.write("A=M" + "\n")
                f.write("M=0" + "\n")
                f.write("(IF_GT_" + str(self._jmp_counter) + "_)" + "\n")
                self._jmp_counter += 1
            elif command == "lt":
                f.write("@IF_LT_" + str(self._jmp_counter) + "_" + "\n")
                f.write("D;JLT" + "\n")
                f.write("@R0" + "\n")
                f.write("A=M" + "\n")
                f.write("M=0" + "\n")
                f.write("(IF_LT_" + str(self._jmp_counter) + "_)" + "\n")
                self._jmp_counter += 1
        elif command in ["and", "or"]:
            f.write("D=M" + "\n")
            f.write("@R0" + "\n")
            f.write("M=M-1" + "\n")
            f.write("A=M" + "\n")
            if command == "and":
                f.write("M=D&M" + "\n")
            elif command == "or":
                f.write("M=D|M" + "\n")
        f.write("@R0" + "\n")
        f.write("M=M+1" + "\n")

    def writePushPop(self, command, segment, index):
        f = self.file
        f.write("// " + command + " " + segment + " " + index + "\n")
        if command == "push":
            if segment == "constant":
                f.write("@" + index + "\n")
                f.write("D=A" + "\n")
            elif segment in ["local", "argument", "this", "that", "temp"]:
                if segment == "temp":
                    f.write("@R5" + "\n")
                    f.write("D=A" + "\n")
                else:
                    mp = {"local": "@R1", "argument": "@R2",
                          "this": "@R3", "that": "@R4"}
                    f.write(mp[segment] + "\n")
                    f.write("D=M" + "\n")
                f.write("@" + index + "\n")
                f.write("A=D+A" + "\n")
                f.write("D=M" + "\n")
            elif segment == "static":
                f.write("@" + self.file_id + "." + self.vm_title + "$" + index + "\n")
                f.write("D=M" + "\n")
            elif segment == "pointer":
                if index == "0":  # "THIS"
                    f.write("@R3" + "\n")
                else:
                    f.write("@R4" + "\n")
                f.write("D=M" + "\n")
            f.write("@R0" + "\n")
            f.write("A=M" + "\n")
            f.write("M=D" + "\n")
            f.write("@R0" + "\n")
            f.write("M=M+1" + "\n")
        else: # pop
            f.write("@R0" + "\n")
            f.write("M=M-1" + "\n")
            # f.write("D=M" + "\n")
            if segment in ["local", "argument", "this", "that", "temp"]:
                if segment == "temp":
                    f.write("@R5" + "\n")
                    f.write("D=A" + "\n")
                else:
                    mp = {"local": "@R1", "argument": "@R2",
                          "this": "@R3", "that": "@R4"}
                    f.write(mp[segment] + "\n")
                    f.write("D=M" + "\n")
                f.write("@" + index + "\n")
                f.write("A=D+A" + "\n")
                f.write("D=A" + "\n")
                f.write("@tmp_" + "\n")
                f.write("M=D" + "\n")
                f.write("@R0" + "\n")
                f.write("A=M" + "\n")
                f.write("D=M" + "\n")
                f.write("@tmp_" + "\n")
                f.write("A=M" + "\n")
                f.write("M=D" + "\n")
            elif segment == "static":
                f.write("A=M" + "\n")
                f.write("D=M" + "\n")
                f.write("@" + self.file_id + "." + self.vm_title + "$" + index + "\n")
                f.write("M=D" + "\n")
            elif segment == "pointer":
                f.write("A=M" + "\n")
                f.write("D=M" + "\n")
                if index == "0":  # "THIS"
                    f.write("@R3" + "\n")
                else:
                    f.write("@R4" + "\n")
                f.write("M=D" + "\n")


def main():
    file_name = sys.argv[1]
    if file_name[(len(file_name)-3):] == ".vm":
        output_file_name = file_name[:(len(file_name)-3)] + ".asm"
        vm_list = [file_name]
    elif not ("." in file_name[(len(file_name)-5):]): # directory
        output_dir_name = file_name[:(len(file_name) - int(file_name.endswith("/")))]
        output_file_name = output_dir_name + "/" + output_dir_name.split("/")[-1] + ".asm"
        vm_list = [output_dir_name + "/" + f for f in os.listdir(output_dir_name) if f.endswith(".vm")]
    else: 
        print("input not vm file?")
    # Initialization
    codewriter = CodeWriter(output_file_name)
    codewriter.writeInit()
    for file_name in vm_list:
        print(file_name)
        parser = Parser(file_name)
        codewriter.setVMTitle(file_name.split("/")[-1][:-3])
        while parser.hasMoreCommands():
            parser.advance()
            cmd = parser.current_command
            cmd_type = parser.commandType()
            if cmd_type == "C_ARITHMETIC":
                codewriter.writeArithmetic(cmd)
            elif cmd_type in ["C_PUSH", "C_POP"]:
                codewriter.writePushPop(
                    cmd.split()[0], parser.arg1(), parser.arg2())
            elif cmd_type == "C_GOTO":
                codewriter.writeGoto(cmd.split()[1])
            elif cmd_type == "C_IF":
                codewriter.writeIf(cmd.split()[1])
            elif cmd_type == "C_LABEL":
                codewriter.writeLabel(cmd.split()[1])
            elif cmd_type == "C_FUNCTION":
                codewriter.writeFunction(cmd.split()[1], cmd.split()[2])
            elif cmd_type == "C_CALL":
                codewriter.writeCall(cmd.split()[1], cmd.split()[2])
            elif cmd_type == "C_RETURN":
                codewriter.writeReturn()
            else:
                print("????")
    codewriter.close()


if __name__ == "__main__":
    main()
