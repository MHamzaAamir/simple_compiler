import re
from nltk import CFG, ChartParser


class SimpleCompiler():
    def __init__(self):
        self.token_patterns = {
            "identifier": r"[a-zA-Z_][a-zA-Z0-9_]*",
            "number": r"\b\d+\b",
            "operator": r"[+/\-*]",
            "equals": r"[=]",
            "whitespace": r"\s+",
        }

        grammar = CFG.fromstring("""
        S -> DECLARATION | ASSIGNMENT
        ASSIGNMENT -> 'identifier' 'equals' OPERATION | 'identifier' 'equals' 'number'
        OPERATION -> TERM 'operator' TERM
        TERM -> 'number' | 'indentifier'
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


    
    


    

            