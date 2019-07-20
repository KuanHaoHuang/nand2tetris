#!/usr/bin/python3
import os
import sys
from JackTokenizer import JackTokenizer


class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer 
        self.output_file = output_file
        self.indent = ""

    def _addIndent(self):
        self.indent = self.indent + "  "
    
    def _subIndent(self):
        self.indent = self.indent[2:]

    def _processTag(s):
        if s == "INT_CONST":
            return "integerConstant"
        elif s == "STRING_CONST":
            return "stringConstant"
        else:
            return s.lower()

    def _startTag(self, tagName, top = False):
        self.output_file.write(self.indent + "<" + tagName + ">")
        if not top:
            self.output_file.write(" ")
        else:
            self.output_file.write("\n")


    def _endTag(self, tagName, top = False):
        if not top:
            self.output_file.write(" ")
            self.output_file.write("</" + tagName + ">")
        else:
            self.output_file.write(self.indent + "</" + tagName + ">")
        self.output_file.write("\n")
    
    def _compileSymbol(self, symbol):
        # just to make the code shorter..
        self._startTag("symbol")
        self.output_file.write(symbol)
        self._endTag("symbol")
        self.tokenizer.advance()

    def compileClass(self):
        # 'class'
        self._startTag("class", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_file.write("class")
        self._endTag("keyword")
        self.tokenizer.advance()
        # className
        self._startTag("identifier")
        self.output_file.write(self.tokenizer.identifier())
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
        self.output_file.write(this_class_var)
        self._endTag("keyword")
        self.tokenizer.advance()
        # type
        self._compileType()
        # varName
        self._startTag("identifier")
        self.output_file.write(self.tokenizer.identifier())
        self._endTag("identifier")
        self.tokenizer.advance()
        # ("," varName)*
        while self.tokenizer.current_token == ",":
            self._compileSymbol(self.tokenizer.symbol())
            self._startTag("identifier")
            self.output_file.write(self.tokenizer.identifier())
            self._endTag("identifier")
            self.tokenizer.advance()
        # ";"
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("classVarDec", top = True)

    def compileSubroutine(self):
        this_subr = self.tokenizer.current_token
        # ('constructor'|'function'|'method')
        self._startTag("subroutineDec", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_file.write(this_subr)
        self._endTag("keyword")
        self.tokenizer.advance()
        # ('void'|type)
        if self.tokenizer.current_token == "void":
            self._startTag("keyword")
            self.output_file.write(self.tokenizer.current_token)
            self._endTag("keyword")
            self.tokenizer.advance()
        else: 
            self._compileType()
        # subroutineName
        self._startTag("identifier")
        self.output_file.write(self.tokenizer.identifier())
        self._endTag("identifier")
        self.tokenizer.advance()
        # '('
        self._compileSymbol(self.tokenizer.symbol())
        # parameterList
        self.compileParameterList()
        # ')'
        self._compileSymbol(self.tokenizer.symbol())
        # subroutineBody
        self._startTag("subroutineBody", top = True)
        self._addIndent()
        ## '{'
        self._compileSymbol(self.tokenizer.symbol())
        ## varDec*
        while self.tokenizer.current_token == "var":
            self.compileVarDec()
        ## statements
        self.compileStatements()
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
        # possibly no parameters
        if self.tokenizer.current_token != ")":
            # type
            self._compileType()
            # varName
            self._startTag("identifier")
            self.output_file.write(self.tokenizer.identifier())
            self._endTag("identifier")
            self.tokenizer.advance()
            # ("," type varName)*
            while self.tokenizer.current_token == ",":
                self._compileSymbol(self.tokenizer.symbol()) # ,
                # type
                self._compileType()
                # varName
                self._startTag("identifier")
                self.output_file.write(self.tokenizer.identifier())
                self._endTag("identifier")
                self.tokenizer.advance()
        # ending
        self._subIndent()
        self._endTag("parameterList", top = True)
    
    def _compileType(self):
        if self.tokenizer.current_token in {"int", "char", "boolean"}:
            self._startTag("keyword")
            self.output_file.write(self.tokenizer.current_token)
            self._endTag("keyword")
            self.tokenizer.advance()
        else: # className
            self._startTag("identifier")
            self.output_file.write(self.tokenizer.identifier())
            self._endTag("identifier")
            self.tokenizer.advance()

    def compileVarDec(self):
        # 'var'
        self._startTag("varDec", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_file.write("var")
        self._endTag("keyword")
        self.tokenizer.advance()
        # type
        self._compileType()
        # varName
        self._startTag("identifier")
        self.output_file.write(self.tokenizer.identifier())
        self._endTag("identifier")
        self.tokenizer.advance()
        # ("," varName)*
        while self.tokenizer.current_token == ",":
            self._compileSymbol(self.tokenizer.symbol())
            self._startTag("identifier")
            self.output_file.write(self.tokenizer.identifier())
            self._endTag("identifier")
            self.tokenizer.advance()
        # ";"
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("varDec", top = True)

    def _compileStatement(self):
        if self.tokenizer.current_token == "let":
            self.compileLet()
        elif self.tokenizer.current_token == "while":
            self.compileWhile()
        elif self.tokenizer.current_token == "if":
            self.compileIf()
        elif self.tokenizer.current_token == "do":
            self.compileDo()
        elif self.tokenizer.current_token == "return":
            self.compileReturn()
    
    def compileStatements(self):
        # statements*
        self._startTag("statements", top = True)
        self._addIndent()
        while self.tokenizer.current_token in {"let", "while", "if", "do", "return"}:
            self._compileStatement()
        # ending
        self._subIndent()
        self._endTag("statements", top = True)

    def compileLet(self):
        # 'let'
        self._startTag("letStatement", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_file.write("let")
        self._endTag("keyword")
        self.tokenizer.advance()
        # varName
        self._startTag("identifier")
        self.output_file.write(self.tokenizer.identifier())
        self._endTag("identifier")
        self.tokenizer.advance()
        # expression starts (possibly no...)
        if self.tokenizer.current_token == "[":
            ## '['
            self._compileSymbol(self.tokenizer.symbol())
            ## expression
            self.compileExpression()
            ## ']'
            self._compileSymbol(self.tokenizer.symbol())
        # expression ends
        # '='
        self._compileSymbol(self.tokenizer.symbol())
        # expression
        self.compileExpression()
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
        self.output_file.write("if")
        self._endTag("keyword")
        self.tokenizer.advance()
        # '('
        self._compileSymbol(self.tokenizer.symbol())
        # expression
        self.compileExpression()
        # ')'
        self._compileSymbol(self.tokenizer.symbol())
        # '{'
        self._compileSymbol(self.tokenizer.symbol())
        # statements
        self.compileStatements()
        # '}'
        self._compileSymbol(self.tokenizer.symbol())
        # else starts (possibly no...)
        if self.tokenizer.current_token == "else":
            self._startTag("keyword")
            self.output_file.write("else")
            self._endTag("keyword")
            self.tokenizer.advance()
            ## '{'
            self._compileSymbol(self.tokenizer.symbol())
            ## statements
            self.compileStatements()
            ## '}' 
            self._compileSymbol(self.tokenizer.symbol())
        # else ends
        # ending
        self._subIndent()
        self._endTag("ifStatement", top = True)

    def compileWhile(self):
        # 'while'
        self._startTag("whileStatement", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_file.write("while")
        self._endTag("keyword")
        self.tokenizer.advance()
        # '('
        self._compileSymbol(self.tokenizer.symbol())
        # expression
        self.compileExpression()
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

    def compileDo(self):
        # 'do'
        self._startTag("doStatement", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_file.write("do")
        self._endTag("keyword")
        self.tokenizer.advance()
        # subroutineCall
        self._compileSubroutineCall()
        # ';'
        self._compileSymbol(self.tokenizer.symbol())
        # ending
        self._subIndent()
        self._endTag("doStatement", top = True)

    def compileReturn(self):
        # 'return'
        self._startTag("returnStatement", top = True)
        self._addIndent()
        self._startTag("keyword")
        self.output_file.write("return")
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
    
    def _compileSubroutineCall(self):
        # subroutineName
        self._startTag("identifier")
        self.output_file.write(self.tokenizer.symbol())
        self._endTag("identifier")
        self.tokenizer.advance()
        if self.tokenizer.current_token == ".":
            self._compileSymbol(self.tokenizer.symbol())
            self._startTag("identifier")
            self.output_file.write(self.tokenizer.current_token)
            self._endTag("identifier")
            self.tokenizer.advance()
        # '('
        self._compileSymbol(self.tokenizer.symbol())
        # expressionList
        self.compileExpressionList()
        # ')'
        self._compileSymbol(self.tokenizer.symbol())
    
    def compileTerm(self):
        # 'term'
        self._startTag("term", top = True)
        self._addIndent()
        tk = self.tokenizer.current_token
        if tk in {"-", "~"}:
            self._compileSymbol(self.tokenizer.current_token)
            self.compileTerm()
        elif tk == "(":
            self._compileSymbol(self.tokenizer.current_token) # (
            self.compileExpression()
            self._compileSymbol(self.tokenizer.current_token) # )
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            pk = self.tokenizer.peek()
            self._startTag("identifier")
            self.output_file.write(self.tokenizer.current_token)
            self._endTag("identifier")
            self.tokenizer.advance()
            if pk == "[": # array
                self._compileSymbol(self.tokenizer.symbol()) # [
                self.compileExpression()
                self._compileSymbol(self.tokenizer.symbol()) # ]
            elif pk == "(": # function
                self._compileSymbol(self.tokenizer.symbol()) # (
                self.compileExpressionList()
                self._compileSymbol(self.tokenizer.symbol()) # )
            elif pk == ".": # method, static method
                self._compileSymbol(self.tokenizer.symbol()) # .
                self._startTag("identifier")
                self.output_file.write(self.tokenizer.current_token)
                self._endTag("identifier")
                self.tokenizer.advance()
                self._compileSymbol(self.tokenizer.symbol()) # (
                self.compileExpressionList()
                self._compileSymbol(self.tokenizer.symbol()) # )
        elif self.tokenizer.tokenType() == "STRING_CONST": 
            self._startTag("stringConstant")
            self.output_file.write(self.tokenizer.stringVal())
            self._endTag("stringConstant")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "INT_CONST": 
            self._startTag("integerConstant")
            self.output_file.write(self.tokenizer.current_token)
            self._endTag("integerConstant")
            self.tokenizer.advance()
        elif self.tokenizer.tokenType() == "KEYWORD": 
            self._startTag("keyword")
            self.output_file.write(self.tokenizer.current_token)
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
        while self.tokenizer.current_token in {"+", "-", "*", "/", 
                                               "&", "|", "<", ">", "="}:
            self._compileSymbol(self.tokenizer.symbol()) 
            self.compileTerm()
        # ending
        self._subIndent()
        self._endTag("expression", top = True)

    def compileExpressionList(self):
        # 'expressionList'
        self._startTag("expressionList", top = True)
        self._addIndent()
        # possibly no...
        if self.tokenizer.current_token != ")":
            # expression
            self.compileExpression()
            # (',' expression)*
            while self.tokenizer.current_token != ")":
                self._compileSymbol(self.tokenizer.symbol()) 
                self.compileExpression()
        # ending
        self._subIndent()
        self._endTag("expressionList", top = True)



