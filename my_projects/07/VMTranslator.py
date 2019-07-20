#!/usr/bin/python3

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
        # f = self.file
        # f.write("// " + "initialize" + "\n")
        # f.write("@256" + "\n")
        # f.write("D=A" + "\n")
        # f.write("@SP" + "\n")
        # f.write("M=D" + "\n")

    def close(self):
        self.file.close()

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
                f.write("@" + self.file_id + "." + index + "\n")
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
                f.write("@" + self.file_id + "." + index + "\n")
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
    else:
        print("input not vm file?")
    # Initialization
    parser = Parser(file_name)
    codewriter = CodeWriter(output_file_name)
    while parser.hasMoreCommands():
        parser.advance()
        cmd = parser.current_command
        cmd_type = parser.commandType()
        if cmd_type == "C_ARITHMETIC":
            codewriter.writeArithmetic(cmd)
        elif cmd_type in ["C_PUSH", "C_POP"]:
            codewriter.writePushPop(
                cmd.split()[0], parser.arg1(), parser.arg2())
        else:
            print("????")
    codewriter.close()


if __name__ == "__main__":
    main()
