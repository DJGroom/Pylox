import Scanner
import VisitorPattern
import Statements
#Some of the following code is inspired from the book and the programmer JHonker's implementation of Parser when building his interpreter.




#RULE SET
#expression     → equality ;
#equality       → comparison ( ( "!=" | "==" ) comparison )* ;
#comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
#term           → factor ( ( "-" | "+" ) factor )* ;
#factor         → unary ( ( "/" | "*" ) unary )* ;
#unary          → ( "!" | "-" ) unary
#               | primary ;
#primary        → NUMBER | STRING | "true" | "false" | "nil"
#               | "(" expression ")" ;
class Parser:
    def __init__(self, tokenlist, inheritor):

        self.current = 0
        #Represents the starting index for teh token list

        self.tokenlist = tokenlist
        #this Token list is the token list provided by the scanner. It holds the entire source code that has been tokenized.
        #We are going to index through the list and build expressions out of the tokens till we hit the end of file token.

    def parse(self):
        #Now this parse method will instead create a list of statements by scanning for keyword tokens such as PRINT,
        #and begin the process of bulding statements through the expression method till we reach the end of teh token list.
        statements = []   
        while not self.at_end():
            statements.append(self.statement())
            
        return statements
    
    def statement(self):
        #Simple method to break up program into statements.
        if(self.match(Scanner.TokenType.PRINT)):
            return self.print_statement()
        else:
            return self.expression_statement()
        
    def print_statement(self):
        #Both the print and expression statement methods do the same thing, first they build an expression found in the statement
        #through the expression method we've already created, then we return teh statement to the statement method we called eariler 
        #to add the statement to the list of statements. 
        expression = self.expression()
        self.consume(Scanner.TokenType.SEMICOLON)
        return Statements.PrintState(expression)
    def expression_statement(self):
        expression = self.expression()
        self.consume(Scanner.TokenType.SEMICOLON)
        return Statements.ExpressionState(expression)
        

    def match(self, *list_of_tokentypes):
        #This method is pretty cool, it takes any number of tokens and calls the check token type to see if the token matchs
        #If any token matchs the we advance to the next token and return true. Else we return false.
        #The fact that match advances is a critical function that keeps the recursion going
        for Token in list_of_tokentypes:
            if (self.check_token_type(Token)):
                self.advance()
                return True
        return False

    def at_end(self):
        #This method checks to see if the next token is the end of the file token, if it is, the program will return true.
        if(self.peek().type == Scanner.TokenType.EOF):
            return True
        else:
            return False

    def check_token_type(self, type):
        #This method simply checks to see if the provided token equals the next token in the list of tokens. 
        if self.at_end():
            return False
        else:
            return self.peek().type == type


    def peek(self):
        #This method returns the current index of teh list. As 'current' is the next token we are choosing,
        #This will cause us to return a token we have yet to consume.
        return self.tokenlist[self.current]

    def previous(self):
        #Look at the previous token
        return self.tokenlist[self.current - 1]

    def advance(self):
        #This method is simple, advance current so that we look at the next token in the token list
        self.current += 1
        return self.previous()

    def expression(self):
        #this according to the rules simply calls equality
        return self.equality()

    '''
    The following needs a fairly large explanation. Instead of commenting on each individual function that has almost identical 
    functionality. I will be giving a summary of what is happening:
    At the start of equality we call the following functions till we get to the primary function, then we will return one of the 
    following 'if' statements that return a literal and advance the current index to the next token-due to how match is built. I need
    to mention that as we call 'match' we are refreshing the token we are comparing to. This functionality is how we stay in recursion 
    Then as we fall back down the cursive tree we will probably get caught again on one of the 'while' statements in the functions 
    because one of the following tokens will match. After advancing to the next token, we save the previous token in that function and 
    climb up the recursive tree again. When we reach primary-the top of the recursion tree-and don't get stuck on anymore functions and 
    return to the original function we got caught on, we will take the literal we got from the primary and build a binary function, and 
    begin to climb back down the recursive tree once again. Now, we will only reach the bottom of the tree if something doesn't match
    in the while loop. As we return the final expression to the expression function, we will be returning the a expression that holds
    expressions. The list of tokens  have been transmorgified into this expression. Thus, as we call the ASTprinter in Pylox.py, we 
    already have our expression needed to build the resulting string and print it to the terminal.
    
    If you find my unclear and unprecise explanation too confusing, I would love to talk more in detail about it.
    '''
    def equality(self):
        #Here we call the comparison function, and if the next token matches band-equal we advance and climb our way up to primary again
        #Thus, at the end we return another expression that we will be able to build a binary erxpression out of, enabling us to return it
        #to the previous caller. 
        expression = self.comparison()
        while(self.match(Scanner.TokenType.BANG_EQUAL, Scanner.TokenType.EQUAL_EQUAL)):
            operator = self.previous()
            rhs = self.comparison()
            expression = VisitorPattern.Binary(expression, operator, rhs)
        return expression
    def comparison(self):
        #The same function above holds the same functionality but different tokens
        expression = self.term()
        while(self.match(Scanner.TokenType.GREATER, Scanner.TokenType.GREATER_EQUAL, Scanner.TokenType.LESS_EQUAL, Scanner.TokenType.LESS)):
            operator = self.previous()
            rhs = self.term()
            expression = VisitorPattern.Binary(expression, operator, rhs)
        return expression
    def term(self):
        #It is important to mention that the reason we call our function in the way we do it to ensure we stand be our rules of presedence 
        #mentioned at the top. 
        expression = self.factor()
        while(self.match(Scanner.TokenType.MINUS, Scanner.TokenType.PLUS)):
            operator = self.previous()
            rhs = self.factor()
            expression = VisitorPattern.Binary(expression, operator, rhs)
        return expression
    def factor(self):
        expression = self.unary()
        while(self.match(Scanner.TokenType.SLASH, Scanner.TokenType.STAR)):
            operator = self.previous()
            rhs = self.unary()
            expression = VisitorPattern.Binary(expression, operator, rhs)
        return expression

    def unary(self):
        #this unary function is unique, we don't want to call teh next function immediately beacuse we want to see if 
        #there is more recursion happening in unary. If there is no recursion happening in unary, we call primary.
        #Note that we aren't calling an extra function in unary because there is no other function that has presedence 
        #primary which we already call
        if self.match(Scanner.TokenType.BANG,Scanner.TokenType.MINUS):
            operator = self.previous()
            rhs = self.unary()
            return VisitorPattern.Unary(operator, rhs)
        else:
            #Or go down the recursive ladder to primary and return the result of primary
            return self.primary()
            
    def primary(self):
        #This is the top of teh recursion ladder. This function must catch all tokens when the token-list is passed to it
        #The function itself in idea it very simple-compare the current index of 
        if(self.match(Scanner.TokenType.NULL)):
            return VisitorPattern.Literal(None)
        elif(self.match(Scanner.TokenType.TRUE)):
            return VisitorPattern.Literal(True)
        elif(self.match(Scanner.TokenType.FALSE)):
            return VisitorPattern.Literal(False)
        elif(self.match(Scanner.TokenType.NUMBER)):
            return VisitorPattern.Literal(self.previous().literal)
        elif(self.match(Scanner.TokenType.STRING)):
            return VisitorPattern.Literal(self.previous().literal)
            #I am not a hunderd percent sure I undertand the following grouping method
        elif(self.match(Scanner.TokenType.LEFT_PAREN)):
            #If we have a paren. that means we have a grouping expression, so we need to call expression again to store the expression,
            #when we come back to this method, we will create th grouping expression and return it.
            expression = self.expression()
            self.consume(Scanner.TokenType.RIGHT_PAREN)
            return VisitorPattern.Group(expression)
        else:
            #simply debug statement
            print("oops")
            return "Oops"
            
    def consume(self, tokentype):
        #If the token matchs, advance
        if(self.check_token_type(tokentype)):
            return self.advance()