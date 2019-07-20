#!/usr/bin/python3
import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

class JackAnalyzer:
    def __init__(self, input_path):
        self.output_dir = "/Users/WilsonHuang/Downloads/nand2tetris/projects/11/my_vm_files/"
        if input_path.endswith(".jack"):
            file_list = [input_path]
        else:
            input_dir_name = input_path + ("" if input_path.endswith("/") else "/")
            file_list = [input_dir_name + f for f in os.listdir(input_dir_name) if f.endswith(".jack")]
        self.file_list = file_list

    def hasMoreFile(self):
        return len(self.file_list) > 0

    def compileOneFile(self):
        if len(self.file_list) == 0:
            print("No more file to be compiled!")
            return False
        input_file_name = self.file_list.pop()
        output_xml_file = open(self.output_dir + input_file_name.split("/")[-1].split(".")[0] + ".xml", "w")
        output_vm_file = open(self.output_dir + input_file_name.split("/")[-1].split(".")[0] + ".vm", "w")
        tokenizer = JackTokenizer(input_file_name)
        compeng = CompilationEngine(tokenizer, output_vm_file, output_xml_file)
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            compeng.compileClass()
        output_vm_file.close()
        output_xml_file.close()
        if True: # well, I wrote the xml file but delete it, cuz it's messy
            os.remove(self.output_dir + input_file_name.split("/")[-1].split(".")[0] + ".xml")
        print("done:  " + input_file_name)

def main():
    ja = JackAnalyzer(sys.argv[1])
    while ja.hasMoreFile():
        ja.compileOneFile()

if __name__ == "__main__":
    main()