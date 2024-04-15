
class Token:
    def __init__(self, type1, line, column, lexeme, literal):
        #All the values of the token class we want, pretty self explanitory
        self.line = line
        self.column = column
        self.type = type1
        self.literal = literal 
        #lexeme here refers to all the characters in the token provides, which is different from the value they represent. For example. "Three" a lexeme, has an actual value of 3
        self.lexeme = lexeme
        
