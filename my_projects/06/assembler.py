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
        ## use this function only if hasMoreCommands
        line = self.file[self.index+1].strip()
        while (len(line) == 0 or line[0] == "/"):
            self.file.pop(self.index + 1)
            line = self.file[self.index+1].strip()
        if line.find("/") >= 0:
            self.current_command = line[0:line.find("/")].strip()
        else:
            self.current_command = line.strip()
        if self.current_command is not None and \
            len(self.current_command) > 0 and \
            self.commandType() != "L_COMMAND":
            self.index = self.index + 1
        else:
            self.file.pop(self.index + 1)
        return
    
    def commandType(self):
        assert self.current_command is not None and len(self.current_command) > 0
        if self.current_command[0] == "@":
            return "A_COMMAND"
        elif self.current_command[0] == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"
    
    def symbol(self):
        assert self.commandType() == "A_COMMAND" or \
            self.commandType() == "L_COMMAND"
        if self.current_command[0] == "@":
            return self.current_command[1:]
        else:
            return self.current_command[1:(len(self.current_command)-1)]
    
    def dest(self):
        assert self.commandType() == "C_COMMAND"
        pos_colon = self.current_command.find(";")
        pos_equal = self.current_command.find("=")
        if pos_equal > 0:
            return self.current_command[0:pos_equal]
        else:
            return "null"

    def comp(self):
        assert self.commandType() == "C_COMMAND"
        pos_colon = self.current_command.find(";")
        pos_equal = self.current_command.find("=")
        if pos_equal > 0:
            pos_start = pos_equal + 1
        else:
            pos_start = 0
        if pos_colon > 0:
            pos_end = pos_colon
        else:
            pos_end = len(self.current_command)
        return self.current_command[pos_start:pos_end]

    def jump(self):
        assert self.commandType() == "C_COMMAND"
        pos_colon = self.current_command.find(";")
        pos_equal = self.current_command.find("=")
        if pos_colon > 0:
            return self.current_command[(pos_colon+1):]
        else:
            return "null"
    
class Code:
    def __init__(self):
        self.comp_table = {
            # left col           # right col
            "0"  : "0"+"101010", 
            "1"  : "0"+"111111",
            "-1" : "0"+"111010",
            "D"  : "0"+"001100",
            "A"  : "0"+"110000", "M"  : "1"+"110000",
            "!D" : "0"+"001101",
            "!A" : "0"+"110001", "!M" : "1"+"110001",
            "-D" : "0"+"001111",
            "-A" : "0"+"110011", "-M" : "1"+"110011",
            "D+1": "0"+"011111",
            "A+1": "0"+"110111", "M+1": "1"+"110111",
            "D-1": "0"+"001110",
            "A-1": "0"+"110010", "M-1": "1"+"110010",
            "D+A": "0"+"000010", "D+M": "1"+"000010",
            "D-A": "0"+"010011", "D-M": "1"+"010011",
            "A-D": "0"+"000111", "M-D": "1"+"000111",
            "D&A": "0"+"000000", "D&M": "1"+"000000",
            "D|A": "0"+"010101", "D|M": "1"+"010101"
        }
        self.dest_table = {
            "null": "000",
            "M"  :  "001",
            "D"  :  "010",
            "MD" :  "011",
            "A"  :  "100",
            "AM" :  "101",
            "AD" :  "110",
            "AMD":  "111"
        }
        self.jump_table = {
            "null": "000",
            "JGT" : "001",
            "JEQ" : "010",
            "JGE" : "011",
            "JLT" : "100",
            "JNE" : "101",
            "JLE" : "110",
            "JMP" : "111"
        }
        return
    
    def dest(self, mnemonic):
        return self.dest_table["".join([e for e in mnemonic if e != " "])]
    
    def comp(self, mnemonic):
        return self.comp_table["".join([e for e in mnemonic if e != " "])]

    def jump(self, mnemonic):
        return self.jump_table["".join([e for e in mnemonic if e != " "])]

class SymbolTable:
    def __init__(self):
        self.table = {("R"+str(i)): i for i in range(16)}
        self.table["SCREEN"] = 16384
        self.table["KBD"] = 24576
        self.table["SP"] = 0
        self.table["LCL"] = 1
        self.table["ARG"] = 2
        self.table["THIS"] = 3
        self.table["THAT"] = 4
        return

    def addEntry(self, symbol, address):
        self.table[symbol] = address
        return
    
    def contains(self, symbol):
        return symbol in self.table
    
    def getAddress(self, symbol):
        return self.table[symbol]

def main():
    file_name = sys.argv[1]
    # Initialization
    parser = Parser(file_name)
    symbol_table = SymbolTable()
    code = Code()
    # First Pass
    while parser.hasMoreCommands():
        parser.advance()
        if parser.commandType() == "L_COMMAND":
            symbol_table.addEntry(parser.symbol(), parser.index+1)
    # Restart reading and translating commands 
    #   Main Loop:
    #   Get the next Assembly Language Command and parse it
    #   For A-commands: Translate symbols to binary addresses
    #   For C-commands: get code for each part and put them together
    #   Output the resulting machine language command
    parser = Parser(file_name)
    n = 16
    new_file_name = file_name.split(".asm")[0] + ".hack"
    with open(new_file_name, 'w') as f:
        f.write("")
    f = open(new_file_name, "a")
    while parser.hasMoreCommands():
        parser.advance()
        if parser.commandType() == "A_COMMAND":
            if symbol_table.contains(parser.symbol()):
                f.write("0"+f"{symbol_table.getAddress(parser.symbol()):015b}"+"\n")
            else:
                if parser.symbol().isnumeric():
                    f.write("0"+f"{int(parser.symbol()):015b}"+"\n")
                else:
                    symbol_table.addEntry(parser.symbol(), n)
                    f.write("0"+f"{n:015b}"+"\n")
                    n = n + 1
        elif parser.commandType() == "C_COMMAND":
            f.write("111" + \
                    code.comp(parser.comp()) + \
                    code.dest(parser.dest()) + \
                    code.jump(parser.jump()) + \
                    "\n")
    f.close()
    return



if __name__ == "__main__":
    main()