#!/usr/bin/python3

class SymbolTable:
    def __init__(self):
        # tbl: {name: (type, kind, index)}
        self.tbl_c = {} # class-level
        self.tbl_s = {} # subroutine-level

    def startSubroutine(self):
        self.tbl_s = {}
    
    def define(self, name, type, kind):
        if kind in {"STATIC", "FIELD"}:
            self.tbl_c[name] = (type, kind, self.varCount(kind))
        elif kind in {"ARG", "VAR"}:
            self.tbl_s[name] = (type, kind, self.varCount(kind))
        else:
            print("???????")
            return None

    def varCount(self, kind):
        # kind is in ("STATIC", "FIELD", "ARG", "VAR")
        if kind in {"STATIC", "FIELD"}:
            return sum([1 for _, tpl in self.tbl_c.items() if tpl[1] == kind]) 
        elif kind in {"ARG", "VAR"}:
            return sum([1 for _, tpl in self.tbl_s.items() if tpl[1] == kind]) 
        else:
            print("???????")
            return None

    def kindOf(self, name):
        if name in self.tbl_s:
            return self.tbl_s[name][1]
        elif name in self.tbl_c:
            return self.tbl_c[name][1]
        else:
            return "NONE"

    def typeOf(self, name):
        if name in self.tbl_s:
            return self.tbl_s[name][0]
        elif name in self.tbl_c:
            return self.tbl_c[name][0]
        else:
            return None

    def indexOf(self, name):
        if name in self.tbl_s:
            return self.tbl_s[name][2]
        elif name in self.tbl_c:
            return self.tbl_c[name][2]
        else:
            return None