from Token import Token
from TokenType import TokenType


class Scanner:
    def __init__(self, code, inheritor):
        #I swapped the variable for code to source because i thought it was more accurate 
        # and it allows me to differentiate between the two files
        self.source = code
        #This is the list of tokens we will be storing
        self.tokens = []
        #absolute position is supposed to represent the array location in the source code, 
        # but I don't really use it. I just included it because it was in the slides.
        self.abs_pos = 0
        self.line = 1
        self.column = 0
        #We start with column zero since the first advance already adds 1 to the column for us. 
        self.start = 0
        #Position in the array where we start to read the following token
        self.current = 0
        #Position in the array where we are reading the characters for the next token
        # I was having a problem reading digits with isdigits() method provided by python 
        # so i took some inspiration from Esamanoaz who made a list and simply compared the characters with
        #creating a list of numbers and letters for comparison 
        self.digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
                        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.keywords = { 
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'for': TokenType.FOR,
            'nil': TokenType.NULL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS, 
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE
    }
    def advance(self):
        #Advance our position in the array by one and increment the column number
        self.current += 1
        self.column += 1
        #While it seems counter-intuitive to subtract one, it is 
        # necesary because we will miss the first array location 0 if we don't.
        #this is also why peek and peek next only look at current and current + 1, 
        # so we don't look further then the array length allows
        return self.source[self.current - 1]
    
    
    def at_end(self):
        #Here, if our current token is at the end of teh array for our code, 
        # we want to return true so that we end the loop of scaning the file
        if(self.current >= len(self.source)):
            return True
        else:
            return False
        
    def peek(self):
        #Here we only want to return the charcter of the current index 
        # if it is in the bounds of teh array for our source code
        if(self.current >= len(self.source)):
            return 0
        else:
            return self.source[self.current]
    
    
    def peek_next(self):
        #Simply the same as peek but looking at the next next character, not fully implemented yet
        return self.source[self.current + 1]
    

    

    def scan_file(self):
        #This will be done till I reach the end of the file
        while not self.at_end():
            #While I am reading the array of chars from the file, I begin to scan for a token. This will be done till I reach the end of the file
            self.scan_token()
            #While I am reading the array of chars from the file, I begin to scan for a token, 
            # I change start to the current position i'm at, which prepares me for the next token
            self.start = self.current     
        self.tokens.append(Token(TokenType.EOF, self.line, self.column, ' ', None))
        #When I am at teh end of the using the at_end method, I need to add a EOF token signifing the end of teh file. 
        return self.tokens
        #It is important that i return the list of tokens I created so that they can be printed to the terminal. 
    
    
    
    
    def scan_token(self):
        #First we advance to teh next char in the array of our source code
        next_char = self.advance()
#After reading the next char in the array, I need to compare the character to see if it matches a known token. Then I need to append that token to the list of tokens I have
#so I can read from it later
        if(next_char == ' '):
            #Do nothing
            x =1
        elif(next_char == '('):
            self.tokens.append(Token(TokenType.LEFT_PAREN, self.line, self.column, '(', None))
        elif(next_char == ')'):
            self.tokens.append(Token(TokenType.RIGHT_PAREN, self.line, self.column, ')', None))
        elif(next_char == '{'):
            self.tokens.append(Token(TokenType.LEFT_BRACE, self.line, self.column, '{', None))
        elif(next_char == '}'):
            self.tokens.append(Token(TokenType.RIGHT_BRACE, self.line, self.column, '}', None))
        elif(next_char == ','):
            self.tokens.append(Token(TokenType.COMA, self.line, self.column, ',', None))
        elif(next_char == '.'):
            self.tokens.append(Token(TokenType.DOT, self.line, self.column, '.', None))
        elif(next_char == '-'):
            self.tokens.append(Token(TokenType.MINUS, self.line, self.column, '-', None))
        elif(next_char == '+'):
            self.tokens.append(Token(TokenType.PLUS, self.line, self.column, '+', None))
        elif(next_char == ';'):
            self.tokens.append(Token(TokenType.SEMICOLON, self.line, self.column, ';', None))
        elif(next_char == '/'):
            self.tokens.append(Token(TokenType.SLASH, self.line, self.column, '/', None))
        elif(next_char == '*'):
            self.tokens.append(Token(TokenType.STAR, self.line, self.column, '*', None))
            
#With the Following possible tokens, I first peek to see if there is an equal sign after, signifing a different token. 
#for this token, we have to advance an extra space because we don't want our current and column number to be wrong and append a new token to our list
# If not, we simply add the single character token I see that there is something after, indicating to me
#that the token is an extra space long. Meaning I need to advance again to create a token 
#Take note that we don't want to advance if we are already at the end of teh file
        elif(next_char == '!'):
            if(self.peek() == '='):
                if(not self.at_end()):
                    self.advance()
                self.tokens.append(Token(TokenType.BANG_EQUAL, self.line, self.column, '!=', None))
            else:
                self.tokens.append(Token(TokenType.BANG, self.line, self.column, '!', None))
                
        elif(next_char == '='):
            if(self.peek() == '='):
                if(not self.at_end()):
                    self.advance()
                self.tokens.append(Token(TokenType.EQUAL_EQUAL, self.line, self.column, '==', None))
            else:
                self.tokens.append(Token(TokenType.EQUAL, self.line, self.column, '=', None))
                
        elif(next_char == '>'):
            if(self.peek() == '='):
                if(not self.at_end()):
                    self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, self.line, self.column, '>=', None))
            else:
                self.tokens.append(Token(TokenType.GREATER, self.line, self.column, '>', None))
                
        elif(next_char == '<'):
            if(self.peek() == '='):
                if(not self.at_end()):
                    self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, self.line, self.column, '<=', None))
            else:
                self.tokens.append(Token(TokenType.LESS, self.line, self.column, '<', None))
        #In this moment, we want to grab all digits and .'s so we simply advance 
        # till there isn't any more, then we tokenize that length of the array from the source
        elif(self.is_digit(next_char)):
            #here we want to kepp advancing if the next character is a number or period
            while(self.is_digit(self.peek()) or self.peek() == '.'):
                self.advance()
            #In this line of code we append the string from the start of the 
            # source to teh current location in the array of the source code to 
            self.tokens.append(Token(TokenType.NUMBER, self.line, self.column, self.source[self.start:self.current], float(self.source[self.start:self.current])))
            
        #this is essentiall the same thing as numbers but with letters. Addionally, we don't have to worry about periods 
        #However, after we have our identifer we must compare that identifier to make sure it isn't a keyword, 
        # if it is, we must change that identifer to a keyword instead using a dictionary
        elif(self.is_letter(next_char)):
            while(self.is_letter(self.peek())):   
                self.advance()
            if(self.source[self.start:self.current] in self.keywords):
                    self.tokens.append(Token(self.keywords.get(self.source[self.start:self.current]), self.line, self.column, self.source[self.start:self.current], self.source[self.start:self.current]))
            else:    
                self.tokens.append(Token(TokenType.IDENTIFIER, self.line, self.column, self.source[self.start:self.current], self.source[self.start:self.current]))
    #The following is special because we need to account for going to new lines of code
        elif(next_char == '\n'):
            #As we are starting on a new line, we need to reset the column number and add one to the line number.
            self.line += 1
            self.column = 0
        elif(next_char == '"'):
            while(self.peek() != '"' and not self.at_end()):
                self.advance()
            self.advance()    
            self.tokens.append(Token(TokenType.STRING, self.line, self.column, self.source[self.start + 1:self.current - 1], self.source[self.start:self.current]))
        else:
            print("[ERROR: UNRECOGNIZED TOKEN]", end='')
            print("[Line:", end='')
            print(self.line, end='')
            print("]", end='')
            print("[Column:", end='')
            print(self.column, end=' ')
            print("][char-value][", end= ' ')
            print(next_char, end=' ')
            print("]")
            
    #These methods are just used to compare a char to see if it is 
    # either a number or leetter, and returns true or false based on the result
    def is_digit(self, next_char):
        return next_char in self.digits
    def is_letter(self, next_char):
        return next_char in self.letters