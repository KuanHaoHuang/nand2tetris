#!/usr/bin/python3
import os
import sys

class JackTokenizer:
    def __init__(self, file_path):
        with open(file_path, "r") as f:
            self.file = [l for l in f.readlines() if ((not l.startswith("//")) and (l is not "\n"))]
        # clear all "/** */"-style comments
        rm_ind_list = []
        add_this = False
        for i in range(len(self.file)):
            if "/**" in self.file[i]:
                rm_ind_list.append(i)
                add_this = True
            if "*/" in self.file[i]:
                if i not in rm_ind_list:
                    rm_ind_list.append(i)
                add_this = False
                continue
            if add_this:
                if i not in rm_ind_list:
                    rm_ind_list.append(i)
        self.file = [self.file[i] for i in range(len(self.file)) if i not in rm_ind_list]
        # break sentences into pieces
        token_list = []
        num_set = {ord(str(i)) for i in range(10)}
        chr_set = {i for i in range(ord("a"), ord("z")+1)}.union({i for i in range(ord("A"), ord("Z")+1)})
        chr_set = chr_set.union(["_"]).union(num_set)
        for i, l in enumerate(self.file):
            # clear all "//"-style comments
            if l.find("//") and l.find("\n") and l.find("//") <= l.find("\n"):
                if l.find("//") == 0:
                    continue
                else:
                    self.file[i] = l[:l.find("//")] 
                    l = self.file[i]
            this_token = ""
            str_flag = False
            num_flag = False
            for e in l:
                if e == "\"":
                    if not str_flag:
                        this_token = "\""
                    else:
                        this_token = this_token + "\""
                    str_flag = not str_flag
                    continue
                elif str_flag:
                    this_token = this_token + e
                    continue
                if ord(e) in num_set:
                    this_token = this_token + e
                    num_flag = True
                    continue
                elif num_flag:
                    token_list.append(this_token)
                    this_token = ""
                    num_flag = False
                if ord(e) in chr_set:
                    this_token = this_token + e
                else:
                    if this_token != "":
                        token_list.append(this_token)
                        this_token = ""
                    if e != " " and e != "\t":
                        token_list.append(e)
            if this_token != "":
                token_list.append(this_token)
        self.file = token_list
        self.current_token = None
        self.index = -1

    def peek(self):
        assert self.hasMoreTokens()
        return self.file[self.index + 1]

    def hasMoreTokens(self):
        return (self.index + 1) in range(len(self.file))

    def advance(self):
        # use this function only if hasMoreTokens
        if self.hasMoreTokens():
            self.index = self.index + 1
            self.current_token = self.file[self.index]
        return

    def tokenType(self):
        chr_set = {i for i in range(ord("a"), ord("z")+1)}.union({i for i in range(ord("A"), ord("Z")+1)})
        chr_set = chr_set.union(["_"])
        num_set = {ord(str(i)) for i in range(10)}
        if self.current_token in {'class', 'constructor', 'function', 'method', 
                               'field', 'static', 'var', 'int',
                               'char', 'boolean', 'void', 'true', 'false',
                               'null', 'this', 'let', 'do', 'if', 'else',
                               'while', 'return'}:
            return "KEYWORD"
        elif self.current_token in {'{', '}', '(', ')', '[', ']',
                                    '.', ',', ';', '+', '-', '*',
                                    '/', '&', '|', '<', '>', '=', '~'}:
            return "SYMBOL"
        elif sum([ord(e) in num_set for e in self.current_token]) == len(self.current_token):
            return "INT_CONST"
        elif self.current_token.startswith("\"") and self.current_token.endswith("\""):
            return "STRING_CONST"
        elif len(self.current_token) != 0:
            return "IDENTIFIER"
        else:
            return "????"

    def keyWord(self):
        # use this function only if tokenType is KEYWORD
        return self.current_token.lower()

    def symbol(self):
        # use this function only if tokenType is SYMBOL
        if self.current_token == "<":
            return "&lt;"
        elif self.current_token == ">":
            return "&gt;"
        elif self.current_token == "\"":
            return "&quot;"
        elif self.current_token == "&":
            return "&amp;"
        return self.current_token

    def identifier(self):
        # use this function only if tokenType is IDENTIFIER
        return self.current_token
    
    def intVal(self):
        # use this function only if tokenType is INT_CONST
        return str(int(self.current_token))

    def stringVal(self):
        # use this function only if tokenType is STRING_CONST
        return self.current_token.strip("\"")

def main():
    def processTag(s):
        if s == "INT_CONST":
            return "integerConstant"
        elif s == "STRING_CONST":
            return "stringConstant"
        else:
            return s.lower()
    file_name = sys.argv[1]
    output_file_name = file_name.split("/")[-1].split(".")[0] + ".xml"
    output_file = open("/Users/WilsonHuang/Downloads/nand2tetris/projects/10/" + \
                        output_file_name, "w")
    output_file.write("<tokens>")
    output_file.write("\n")
    tknzr = JackTokenizer(file_name)
    while tknzr.hasMoreTokens():
        tknzr.advance()
        tk = tknzr.current_token
        print("{:13s}".format(tknzr.tokenType()) + "  >>" + tk)
        output_file.write("<" + processTag(tknzr.tokenType()) + ">")
        output_file.write(" ")
        if tknzr.tokenType() == "KEYWORD":
            output_file.write(tknzr.keyWord())
        elif tknzr.tokenType() == "SYMBOL":
            output_file.write(tknzr.symbol())
        elif tknzr.tokenType() == "IDENTIFIER":
            output_file.write(tknzr.identifier())
        elif tknzr.tokenType() == "INT_CONST":
            output_file.write(tknzr.intVal())
        elif tknzr.tokenType() == "STRING_CONST":
            output_file.write(tknzr.stringVal())
        output_file.write(" ")
        output_file.write("</" + processTag(tknzr.tokenType()) + ">")
        output_file.write("\n")
    output_file.write("</tokens>")
    output_file.write("\n")
    output_file.close()

if __name__ == "__main__":
    main()
