#!/usr/bin/python3

class VMWriter():
    def __init__(self, output_file):
        self.output_file = output_file # file stream
        self.seg_dict = {e: e.lower() for e in {"CONST", "ARG", "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"}}
        self.seg_dict["CONST"] = "constant"
        self.seg_dict["ARG"] = "argument"

    def writePush(self, segment, index):
        assert segment in self.seg_dict
        self.output_file.write("push " + self.seg_dict[segment] + " " + str(index) + "\n")
    
    def writePop(self, segment, index):
        assert segment in self.seg_dict
        self.output_file.write("pop " + self.seg_dict[segment] + " " + str(index) + "\n")

    def writeArithmetic(self, command):
        assert command in {"ADD", "SUB", "NEG", "EQ", "GT", "LT", "AND", "OR", "NOT"}
        self.output_file.write(command.lower() + "\n")

    def writeLabel(self, label):
        self.output_file.write("label " + label.upper() + "\n")

    def writeGoto(self, label):
        self.output_file.write("goto " + label.upper() + "\n")

    def writeIf(self, label):
        self.output_file.write("if-goto " + label.upper() + "\n")
    
    def writeCall(self, name, nArgs):
        self.output_file.write("call " + name + " " + str(nArgs) + "\n")

    def writeFunction(self, name, nLocals):
        self.output_file.write("function " + name + " " + str(nLocals) + "\n")

    def writeReturn(self):
        self.output_file.write("return" + "\n")
    
    def close(self):
        self.output_file.close()

