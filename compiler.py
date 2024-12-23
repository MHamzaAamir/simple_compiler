import re
from nltk import CFG, ChartParser


class SimpleCompiler():
    def __init__(self):
        self.token_patterns = {
            "number": r"\b\d+\b",
            "operator": r"[+/\-*]",
            "declare": r"\bdeclare\b",
            "while": r"\bwhile\b",
            "if": r"\bif\b",
            "open_paren": r"\(",
            "close_paren": r"\)",
            "open_curly": r"\{",
            "close_curly": r"\}",
            "comparison_op": r"(==|>=|<=|>|<)",
            "equals": r"[=]",
            "whitespace": r"\s+",
            "identifier": r"[a-zA-Z_][a-zA-Z0-9_]*",
        }

        grammar = CFG.fromstring("""
        S -> DECLARATION | EXPRESSION 
        DECLARATION -> 'declare' 'identifier'
        
        EXPRESSION -> ASSIGNMENT | CONDITIONAL | LOOP
        
        ASSIGNMENT -> 'identifier' 'equals' TERM 
        TERM -> 'identifier' | 'number' | 'number' 'operator' TERM | 'identifier' 'operator' TERM
        
        CONDITIONAL -> 'if' 'open_paren' CONDITION 'close_paren' 'open_curly' EXPRESSION 'close_curly'
        LOOP -> 'while' 'open_paren' CONDITION 'close_paren' 'open_curly' EXPRESSION 'close_curly'
        
        CONDITION -> 'identifier' 'comparison_op' 'identifier' | 'identifier' 'comparison_op' 'number'
        """)
        self.parser = ChartParser(grammar)
    
    def load_file(self,file_path):
        with open(file_path,'r') as file:
            return file.readlines()
        
    def tokenize(self,line,line_no):
        tokens = ""
        while(line):
            matched = False
            for token_type, pattern in self.token_patterns.items():
                match = re.match(pattern, line)
                if match:
                    lexeme = match.group()
                    if token_type != "whitespace":
                        if(len(tokens)==0):
                            tokens = token_type
                        else:
                            tokens = tokens + " " + token_type
                    line = line[len(lexeme):]
                    matched = True
                    break
            if not matched:
                raise Exception(f"Unrecognized token at Line: {line_no}")
        return tokens
    
    def validate(self,tokens,line_no):
        tokens = tokens.split()
        trees = self.parser.parse(tokens)
        count = 0
        for tree in trees:
            count += 1
        if count == 0:
            raise Exception(f"Syntax error at Line: {line_no}")
    
    def compile(self,filepath):
        lines = self.load_file(filepath)
        for line_no, line in enumerate(lines, start=1):
            try:
                line = line.strip()
                if not line:
                    continue
                
                tokens = self.tokenize(line,line_no)
                
                self.validate(tokens,line_no) 
            except Exception as e:
                print(e)
                return False

        print("Compilation Was Successful. No Errors")
        return True
     
            

if __name__ == "__main__":
    compiler = SimpleCompiler()
    compiler.compile("code.txt")