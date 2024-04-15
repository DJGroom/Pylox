from enum import Enum, auto


class TokenType(Enum):
    
    #With Enums in python, you have to make your own class, and must be assigned values, even if we have to use the auto() function from ENUM to give them values later
    #I needed a bit a research from Geeks for Geeks on this one
    #All single characters tokens from the slides you gave out
    
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    
    #One or two character tokens
    #One character token
    BANG = auto()
    EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    #two characters token
    BANG_EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    #End of file token. 
    EOF = auto()
    
    #Literals
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    
    #Keywords provided by book
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto() 
    FUN = auto() 
    FOR = auto() 
    IF = auto() 
    NULL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto() 
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    