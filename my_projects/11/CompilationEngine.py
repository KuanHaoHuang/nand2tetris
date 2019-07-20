#!/usr/bin/python3
import os
import sys
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    def __init__(self, tokenizer, output_vm_file, output_xml_file = None):
        self.tokenizer = tokenizer 
        self.vmr = VMWriter(output_vm_file)
        self.output_xml_file = output_xml_file
        self.indent = ""
        self.symbol_table = SymbolTable()
        self.current_class = None
        self.void_subr = set()
        self.label_counter = 0

    def _addIndent(self):
        self.indent = self.indent + "  "
    
    def _subIndent(self):
        self.indent = self.indent[2:]

    def _startTag(self, tagName, top = False):
        self.output_xml_file.write(self.indent + "<" + tagName + ">")
        if not top:
            self.output_xml_file.write(" ")
        else:
            self.output_xml_file.write("\n")

    def _endTag(self, tagName, top = False):
        if not top:
            self.output_xml_file.write(" ")
            self.output_xml_file.write("</" + tagName + ">")
        else:
            self.output_xml_file.write(self.indent + "</" + tagName + ">")
        self.output_xml_file.write("\n")
    
    def _compileSymbol(self, symbol):
        # just to make the code shorter..
        self._startTag("symbol")
        self.output_xml_file.write(symbol)
        self._endTag("symbol")
        self.tokenizer.advance()
        if symbol == "&lt;":
            return "<"
        elif symbol == "&gt;":
            return ">"
        elif symbol == "&quot;":
            return "\""
        elif symbol == "&amp;":
            return "&"
        else:
            return symbol

    def _compileIdentifier(self, name, status, type="", kind = ""):
        is_cs = kind in {"CLASS", "SUBROUTINE"}
        if status == "def":
            assert kind != "" and type != ""
            self.symbol_table.define(name = name, type = type, kind = kind)
        self._startTag("identifier")
        if is_cs:
            self.output_xml_file.write(status + ": " + kind + " " + name)
        else:
            self.output_xml_file.write(status + ": " + ", ".join([name,
                                              "type="+self.symbol_table.typeOf(name),
                                              "kind="+self.symbol_table.kindOf(name),
                                              "index="+str(self.symbol_table.indexOf(name))]))
        self._endTag("identifier")
        self.tokenizer.advance()
        return name

    def _compileType(self):
        if self.tokenizer.current_token in {"int", "char", "boolean"}:
            this_type = self.tokenizer.current_token
            self._startTag("keyword")
            self.output_xml_file.write(self.tokenizer.current_token)
            self._endTag("keyword")
            self.tokenizer.advance()
            return this_type
        else: # className
            this_class = self._compileIdentifier(name = self.tokenizer.identifier(), kind = "CLASS", status = "use")
            return this_class

    def compileClass(self):
        # 'class'
        self._startTag("class", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_xml_file.write("class")
        self._endTag("keyword")
        self.tokenizer.advance()
        # className
        self._startTag("identifier")
        self.output_xml_file.write("onset of class: " + self.tokenizer.current_token)
        self.current_class = self.tokenizer.current_token 
        self._endTag("identifier")
        self.tokenizer.advance()
        # '{'
        self._compileSymbol(self.tokenizer.symbol())
        # classVarDec* subroutineDec*
        while not self.tokenizer.current_token == "}":
            if self.tokenizer.current_token in {"static", "field"}:
                self.compileClassVarDec()
            elif self.tokenizer.current_token in {"constructor", "function", "method"}:
                self.compileSubroutine()
        # '}'
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("class", top = True)

    def compileClassVarDec(self):
        this_class_var = self.tokenizer.current_token
        # {'static'|'field'}
        self._startTag("classVarDec", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_xml_file.write(this_class_var)
        self._endTag("keyword")
        self.tokenizer.advance()
        # type
        this_type = self._compileType()
        # varName
        self._compileIdentifier(name = self.tokenizer.identifier(), type = this_type, kind = this_class_var.upper(), status = "def")
        # ("," varName)*
        while self.tokenizer.current_token == ",":
            self._compileSymbol(self.tokenizer.symbol())
            self._compileIdentifier(name = self.tokenizer.identifier(), type = this_type, kind = this_class_var.upper(), status = "def")
        # ";"
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("classVarDec", top = True)

    def compileSubroutine(self):
        self.symbol_table.startSubroutine()
        this_subr = self.tokenizer.current_token
        # ('constructor'|'function'|'method')
        self._startTag("subroutineDec", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_xml_file.write(this_subr)
        self._endTag("keyword")
        self.tokenizer.advance()
        # ('void'|type)
        this_return_type = self.tokenizer.current_token 
        if self.tokenizer.current_token == "void":
            self._startTag("keyword")
            self.output_xml_file.write(self.tokenizer.current_token)
            self._endTag("keyword")
            self.tokenizer.advance()
        else: 
            self._compileType()
        # subroutineName
        self._startTag("identifier")
        this_subr_name = self.tokenizer.current_token
        self.output_xml_file.write("onset of subroutine: " + self.tokenizer.current_token)
        self._endTag("identifier")
        self.tokenizer.advance()
        if this_return_type == "void":
            self.void_subr.add(this_subr_name)
        # '('
        self._compileSymbol(self.tokenizer.symbol())
        # parameterList
        if this_subr == "method":
            self.symbol_table.define(name = "this", type = self.current_class, kind = "ARG")
        param_cnt = self.compileParameterList() + (this_subr == "method")
        # ')'
        self._compileSymbol(self.tokenizer.symbol())
        # subroutineBody
        self._startTag("subroutineBody", top = True)
        self._addIndent()
        ## '{'
        self._compileSymbol(self.tokenizer.symbol())
        ## varDec*
        lcl_cnt = 0
        while self.tokenizer.current_token == "var":
            lcl_cnt += self.compileVarDec()
        self.vmr.writeFunction(self.current_class + "." + this_subr_name, lcl_cnt)
        if this_subr == "method":
            self.vmr.writePush("ARG", 0)
            self.vmr.writePop("POINTER", 0)
        elif this_subr == "constructor":
            self.vmr.writePush("CONST", len(self.symbol_table.tbl_c))
            self.vmr.writeCall("Memory.alloc", 1)
            self.vmr.writePop("POINTER", 0)
        ## statements
        self.compileStatements(is_void = (this_return_type == "void"))
        ## '}'
        self._compileSymbol(self.tokenizer.symbol())
        ## subroutineBody ending
        self._subIndent()
        self._endTag("subroutineBody", top = True)
        # ending
        self._subIndent()
        self._endTag("subroutineDec", top = True)

    def compileParameterList(self):
        self._startTag("parameterList", top = True)
        self._addIndent()
        param_cnt = 0
        # possibly no parameters
        if self.tokenizer.current_token != ")":
            param_cnt += 1
            # type
            this_type = self._compileType()
            # varName
            self._compileIdentifier(name = self.tokenizer.identifier(), type = this_type, kind = "ARG", status = "def")
            # ("," type varName)*
            while self.tokenizer.current_token == ",":
                param_cnt += 1
                self._compileSymbol(self.tokenizer.symbol()) # ,
                # type
                this_type = self._compileType()
                # varName
                self._compileIdentifier(name = self.tokenizer.identifier(), type = this_type, kind = "ARG", status = "def")
        # ending
        self._subIndent()
        self._endTag("parameterList", top = True)
        return param_cnt

    def compileVarDec(self):
        # 'var'
        self._startTag("varDec", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_xml_file.write("var")
        self._endTag("keyword")
        self.tokenizer.advance()
        # type
        this_type = self._compileType()
        var_cnt = 1
        # varName
        self._compileIdentifier(name = self.tokenizer.identifier(), type = this_type, kind = "VAR", status = "def")
        # ("," varName)*
        while self.tokenizer.current_token == ",":
            var_cnt += 1
            self._compileSymbol(self.tokenizer.symbol())
            self._compileIdentifier(name = self.tokenizer.identifier(), type = this_type, kind = "VAR", status = "def")
        # ";"
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("varDec", top = True)
        return var_cnt

    def _compileStatement(self, is_void = False):
        if self.tokenizer.current_token == "let":
            self.compileLet()
        elif self.tokenizer.current_token == "while":
            self.compileWhile()
        elif self.tokenizer.current_token == "if":
            self.compileIf()
        elif self.tokenizer.current_token == "do":
            self.compileDo()
        elif self.tokenizer.current_token == "return":
            self.compileReturn(is_void = is_void)
    
    def compileStatements(self, is_void=False):
        # statements*
        self._startTag("statements", top = True)
        self._addIndent()
        while self.tokenizer.current_token in {"let", "while", "if", "do", "return"}:
            self._compileStatement(is_void=is_void)
        # ending
        self._subIndent()
        self._endTag("statements", top = True)

    def compileLet(self):
        # 'let'
        self._startTag("letStatement", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_xml_file.write("let")
        self._endTag("keyword")
        self.tokenizer.advance()
        # varName
        this_var = self._compileIdentifier(name = self.tokenizer.identifier(), status = "use")
        # expression starts (possibly no...)
        is_arr = False
        if self.tokenizer.current_token == "[":
            is_arr = True
            if self.symbol_table.kindOf(this_var) == "VAR":
                self.vmr.writePush("LOCAL", self.symbol_table.indexOf(this_var))
            elif self.symbol_table.kindOf(this_var) == "ARG":
                self.vmr.writePush("ARG", self.symbol_table.indexOf(this_var))
            elif self.symbol_table.kindOf(this_var) == "FIELD":
                self.vmr.writePush("THIS", self.symbol_table.indexOf(this_var))
            elif self.symbol_table.kindOf(this_var) == "STATIC":
                self.vmr.writePush("STATIC", self.symbol_table.indexOf(this_var))
            else:
                pass
            ## '['
            self._compileSymbol(self.tokenizer.symbol())
            ## expression
            self.compileExpression()
            ## ']'
            self._compileSymbol(self.tokenizer.symbol())
            self.vmr.writeArithmetic("ADD")
        # expression ends
        # '='
        self._compileSymbol(self.tokenizer.symbol())
        # expression
        self.compileExpression()
        if is_arr:
            self.vmr.writePop("TEMP", 0)
            self.vmr.writePop("POINTER", 1)
            self.vmr.writePush("TEMP", 0)
            self.vmr.writePop("THAT", 0)
        else:
            if self.symbol_table.kindOf(this_var) == "VAR":
                self.vmr.writePop("LOCAL", self.symbol_table.indexOf(this_var))
            elif self.symbol_table.kindOf(this_var) == "ARG":
                self.vmr.writePop("ARG", self.symbol_table.indexOf(this_var))
            elif self.symbol_table.kindOf(this_var) == "FIELD":
                self.vmr.writePop("THIS", self.symbol_table.indexOf(this_var))
            elif self.symbol_table.kindOf(this_var) == "STATIC":
                self.vmr.writePop("STATIC", self.symbol_table.indexOf(this_var))
            else:
                pass
        # ';'
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("letStatement", top = True)

    def compileIf(self):
        # 'if'
        self._startTag("ifStatement", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_xml_file.write("if")
        self._endTag("keyword")
        self.tokenizer.advance()
        # '('
        self._compileSymbol(self.tokenizer.symbol())
        # expression
        self.compileExpression()
        self.vmr.writeArithmetic("NOT")
        label_1 = self.label_counter
        self.label_counter += 1
        self.vmr.writeIf("IF_LABEL_" + str(label_1)) ## to leave if
        # ')'
        self._compileSymbol(self.tokenizer.symbol())
        # '{'
        self._compileSymbol(self.tokenizer.symbol())
        # statements
        self.compileStatements()
        label_2 = self.label_counter
        self.label_counter += 1
        self.vmr.writeGoto("LEAVE_IF_LABEL_" + str(label_2)) ## to leave if _2
        # '}'
        self._compileSymbol(self.tokenizer.symbol())
        # else starts (possibly no...)
        self.vmr.writeLabel("IF_LABEL_" + str(label_1))
        if self.tokenizer.current_token == "else":
            self._startTag("keyword")
            self.output_xml_file.write("else")
            self._endTag("keyword")
            self.tokenizer.advance()
            ## '{'
            self._compileSymbol(self.tokenizer.symbol())
            ## statements
            self.compileStatements()
            ## '}' 
            self._compileSymbol(self.tokenizer.symbol())
        self.vmr.writeLabel("LEAVE_IF_LABEL_" + str(label_2))
        # else ends
        # ending
        self._subIndent()
        self._endTag("ifStatement", top = True)

    def compileWhile(self):
        # 'while'
        self._startTag("whileStatement", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_xml_file.write("while")
        self._endTag("keyword")
        self.tokenizer.advance()
        label_1 = str(self.label_counter)
        self.label_counter += 1
        self.vmr.writeLabel("WHILE_LABEL_" + label_1)
        # '('
        self._compileSymbol(self.tokenizer.symbol())
        # expression
        self.compileExpression()
        self.vmr.writeArithmetic("NOT")
        label_2 = str(self.label_counter)
        self.label_counter += 1
        self.vmr.writeIf("WHILE_LABEL_" + label_2) ## to leave while
        # ')'
        self._compileSymbol(self.tokenizer.symbol())
        # '{'
        self._compileSymbol(self.tokenizer.symbol())
        # statements
        self.compileStatements()
        # '}'
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("whileStatement", top = True)
        self.vmr.writeGoto("WHILE_LABEL_" + label_1)
        self.vmr.writeLabel("WHILE_LABEL_" + label_2)
        self.label_counter += 1

    def compileDo(self):
        # 'do'
        self._startTag("doStatement", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_xml_file.write("do")
        self._endTag("keyword")
        self.tokenizer.advance()
        # subroutineCall
        self._compileSubroutineCall()
        # ';'
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("doStatement", top = True)

    def compileReturn(self, is_void = False):
        # 'return'
        self._startTag("returnStatement", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_xml_file.write("return")
        self._endTag("keyword")
        self.tokenizer.advance()
        # expression  (possibly no...)
        if self.tokenizer.current_token != ";":
            self.compileExpression()
        # ';'
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("returnStatement", top = True)
        if is_void:
            self.vmr.writePush("CONST", 0)
        self.vmr.writeReturn()
    
    def _compileSubroutineCall(self):
        # subroutineName or className
        pk = self.tokenizer.peek()
        if pk == ".":
            this_head = self._compileIdentifier(name=self.tokenizer.identifier(), kind="CLASS", status="use")
            this_head_type = self.symbol_table.typeOf(this_head) 
            this_head_kind = self.symbol_table.kindOf(this_head) 
            if this_head_kind == "FIELD":
                this_head_kind = "THIS"
            elif this_head_kind == "VAR":
                this_head_kind = "LOCAL"
            if this_head_type is not None: # method
                self._compileSymbol(self.tokenizer.symbol()) # "." 
                subr_name = self._compileIdentifier(
                        name=self.tokenizer.identifier(), kind="SUBROUTINE", status="use")
                this_subr = this_head_type + "." + subr_name
                self.vmr.writePush(this_head_kind, self.symbol_table.indexOf(this_head))
            else: # function
                this_subr = this_head + \
                    self._compileSymbol(self.tokenizer.symbol()) + \
                    self._compileIdentifier(
                        name=self.tokenizer.identifier(), kind="SUBROUTINE", status="use")
        else: # method of current class
            this_subr = self._compileIdentifier(name = self.tokenizer.identifier(), kind = "SUBROUTINE", status = "use")
            this_subr = self.current_class + "." + this_subr
            self.vmr.writePush("POINTER", 0)
        # '('
        self._compileSymbol(self.tokenizer.symbol())
        # expressionList
        exp_cnt = self.compileExpressionList()
        # ')'
        self._compileSymbol(self.tokenizer.symbol())
        self.vmr.writeCall(this_subr, exp_cnt + ((pk == "." and (1 if this_head_type else 0)) or pk != "."))
        self.vmr.writePop("TEMP", 0)
    
    def compileTerm(self):
        # 'term'
        self._startTag("term", top = True)
        self._addIndent()
        tk = self.tokenizer.current_token
        if tk in {"-", "~"}:
            self._compileSymbol(self.tokenizer.current_token)
            self.compileTerm()
            if tk == "-":
                self.vmr.writeArithmetic("NEG")
            elif tk == "~":
                self.vmr.writeArithmetic("NOT")
        elif tk == "(":
            self._compileSymbol(self.tokenizer.current_token) # (
            self.compileExpression()
            self._compileSymbol(self.tokenizer.current_token) # )
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            pk = self.tokenizer.peek()
            self._compileIdentifier(name = self.tokenizer.current_token, kind = "CLASS", status = "use")
            if pk == "[": # array
                if self.symbol_table.kindOf(tk) == "VAR":
                    self.vmr.writePush("LOCAL", self.symbol_table.indexOf(tk))
                elif self.symbol_table.kindOf(tk) == "ARG":
                    self.vmr.writePush("ARG", self.symbol_table.indexOf(tk))
                elif self.symbol_table.kindOf(tk) == "FIELD":
                    self.vmr.writePush("THIS", self.symbol_table.indexOf(tk))
                elif self.symbol_table.kindOf(tk) == "STATIC":
                    self.vmr.writePush("STATIC", self.symbol_table.indexOf(tk))
                else:
                    pass
                self._compileSymbol(self.tokenizer.symbol()) # [
                self.compileExpression()
                self._compileSymbol(self.tokenizer.symbol()) # ]
                self.vmr.writeArithmetic("ADD")
                self.vmr.writePop("POINTER", 1)
                self.vmr.writePush("THAT", 0)
            elif pk == "(": # must be a method
                if self.symbol_table.kindOf(tk) == "VAR":
                    self.vmr.writePush("LOCAL", self.symbol_table.indexOf(tk))
                elif self.symbol_table.kindOf(tk) == "ARG":
                    self.vmr.writePush("ARG", self.symbol_table.indexOf(tk))
                elif self.symbol_table.kindOf(tk) == "FIELD":
                    self.vmr.writePush("THIS", self.symbol_table.indexOf(tk))
                elif self.symbol_table.kindOf(tk) == "STATIC":
                    self.vmr.writePush("STATIC", self.symbol_table.indexOf(tk))
                else:
                    pass
                self._compileSymbol(self.tokenizer.symbol()) # (
                exp_cnt = self.compileExpressionList()
                self._compileSymbol(self.tokenizer.symbol()) # )
                self.vmr.writeCall(self.current_class + "." + tk, exp_cnt + 1)
            elif pk == ".": # method, or function
                self._compileSymbol(self.tokenizer.symbol()) # .
                if self.symbol_table.typeOf(tk): # method
                    this_subr = self._compileIdentifier(name=self.symbol_table.typeOf(tk) + "." + self.tokenizer.current_token,
                                                        kind="SUBROUTINE", status="use")
                    if self.symbol_table.kindOf(tk) == "VAR":
                        self.vmr.writePush("LOCAL", self.symbol_table.indexOf(tk))
                    elif self.symbol_table.kindOf(tk) == "ARG":
                        self.vmr.writePush("ARG", self.symbol_table.indexOf(tk))
                    elif self.symbol_table.kindOf(tk) == "FIELD":
                        self.vmr.writePush("THIS", self.symbol_table.indexOf(tk))
                    elif self.symbol_table.kindOf(tk) == "STATIC":
                        self.vmr.writePush("STATIC", self.symbol_table.indexOf(tk))
                    else:
                        pass
                else:
                    this_subr = self._compileIdentifier(name=tk + "." + self.tokenizer.current_token,
                                                        kind="SUBROUTINE", status="use")
                self._compileSymbol(self.tokenizer.symbol()) # (
                exp_cnt = self.compileExpressionList()
                self._compileSymbol(self.tokenizer.symbol()) # )
                if self.symbol_table.typeOf(tk): # method
                    self.vmr.writeCall(this_subr, exp_cnt + 1)
                else:
                    self.vmr.writeCall(this_subr, exp_cnt)
            else: # identifier
                if self.symbol_table.kindOf(tk) == "VAR":
                    self.vmr.writePush("LOCAL", self.symbol_table.indexOf(tk))
                elif self.symbol_table.kindOf(tk) == "ARG":
                    self.vmr.writePush("ARG", self.symbol_table.indexOf(tk))
                elif self.symbol_table.kindOf(tk) == "FIELD":
                    self.vmr.writePush("THIS", self.symbol_table.indexOf(tk))
                elif self.symbol_table.kindOf(tk) == "STATIC":
                    self.vmr.writePush("STATIC", self.symbol_table.indexOf(tk))
                else:
                    pass
        elif self.tokenizer.tokenType() == "STRING_CONST": 
            self._startTag("stringConstant")
            self.output_xml_file.write(self.tokenizer.stringVal())
            self.vmr.writePush("CONST", len(self.tokenizer.stringVal()))
            self.vmr.writeCall("String.new", 1)
            for s in self.tokenizer.stringVal():
                self.vmr.writePush("CONST", ord(s))
                self.vmr.writeCall("String.appendChar", 2)
            self._endTag("stringConstant")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "INT_CONST": 
            self._startTag("integerConstant")
            self.output_xml_file.write(self.tokenizer.current_token)
            self.vmr.writePush("CONST", self.tokenizer.current_token)
            self._endTag("integerConstant")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "KEYWORD":  # true / false / this / null
            self._startTag("keyword")
            self.output_xml_file.write(self.tokenizer.current_token)
            if self.tokenizer.current_token == "true":
                self.vmr.writePush("CONST", 1)
                self.vmr.writeArithmetic("NEG")
            elif self.tokenizer.current_token == "false" or self.tokenizer.current_token == "null":
                self.vmr.writePush("CONST", 0)
            elif self.tokenizer.current_token == "this":
                self.vmr.writePush("POINTER", 0)
            elif self.tokenizer.current_token == "that":
                self.vmr.writePush("POINTER", 1)
            self._endTag("keyword")
            self.tokenizer.advance()
        else:
            print("????")
        # ending
        self._subIndent()
        self._endTag("term", top = True)

    def compileExpression(self):
        # 'expression'
        self._startTag("expression", top = True)
        self._addIndent()
        # term
        self.compileTerm()
        # (op term)*
        symb_dict = {"+": "ADD", "-": "SUB",
                     "&": "AND", "|": "OR", 
                     "<": "LT", ">": "GT", "=": "EQ"}
        while self.tokenizer.current_token in {"+", "-", "*", "/", 
                                               "&", "|", "<", ">", "="}:
            this_symb = self._compileSymbol(self.tokenizer.symbol()) 
            self.compileTerm()
            if this_symb == "*":
                self.vmr.writeCall("Math.multiply", 2)
            elif this_symb == "/":
                self.vmr.writeCall("Math.divide", 2)
            else:
                self.vmr.writeArithmetic(symb_dict[this_symb])
        
        self._subIndent()
        self._endTag("expression", top = True)

    def compileExpressionList(self):
        # 'expressionList'
        self._startTag("expressionList", top = True)
        self._addIndent()
        exp_cnt = 0
        # possibly no...
        if self.tokenizer.current_token != ")":
            exp_cnt += 1
            # expression
            self.compileExpression()
            # (',' expression)*
            while self.tokenizer.current_token != ")":
                exp_cnt += 1
                self._compileSymbol(self.tokenizer.symbol()) 
                self.compileExpression()
        # ending
        self._subIndent()
        self._endTag("expressionList", top = True)
        return exp_cnt



