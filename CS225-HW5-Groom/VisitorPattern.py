#the Following code is inspired from the refactoring guru Visitor implementation you sent out by email and a little bit from kathleenbanawa 
#beacuse I had trouble getting the string to properly print out. 
from __future__ import annotations
from abc import ABC, abstractmethod
from Token import Token
from TokenType import TokenType
from Statements import Statement
from Statements import PrintState
from Statements import ExpressionState

class Expression:

    #Here we declare the base class for teh expressions. These accept methods are described in the child class, but I find it helpful to see them here
    pass

    

class Binary(Expression):
    #For each expression I did something unique, instead of using the accept method in teh parenthesize method, I simply created a a string method
    #This new approach was inspired by kathleenbanawa. More specifcally the __str__ method. I didn't take the same approach as him since he used the accept method in PARENTHESIZE


    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        #Here we simply declare variables and assign them in teh class


    def accept(self, visitor: Visitor):
        return visitor.visit_binary(self)
    #these accept methods pass the member data and member functions of teh expression class into the teh visitor which allows us to build a string in the ASTPRINTER

    def __str__(self):
        return f"{self.operator.lexeme} {self.left} {self.right}"
    #This is teh unique function I created in each expression class so I can simply call it to help build my string 
class Literal(Expression):

    def __init__(self, value):
        self.value = value


    def accept(self, visitor: Visitor):
        return visitor.visit_literal(self)
#The string method here creates a string that can be passed into teh parenthisize method that is used to print the final expression
    def __str__(self):
        return f"{self.value}"
class Unary(Expression):
    def __init__(self, operator, expre):
        self.operator = operator
        self.expre = expre

    def __str__(self):
        return f"{self.operator.lexeme} {self.expre}"

    def accept(self, visitor: Visitor):
        return visitor.visit_unary(self)


class Group(Expression):
    #Group expression here does something unique. Because I know that what I am returning in my string method will be used to create the final expresion.
    #I created a new member data caled name that helps print group so that my expression can be seen. 
    def __init__(self, expre):
        self.name = "group"
        self.expre = expre

    def __str__(self):
        return f"{self.name} ({self.expre})"

    def accept(self, visitor: Visitor):
        return visitor.visit_group(self)
        
class Visitor(ABC):
    #The folowing abstract methods are here so that the ASTprinter class can fully implement them in its class

    @abstractmethod
    def visit_binary(self, element: Binary):
        pass

    @abstractmethod
    def visit_unary(self, element: Unary):
        pass
    @abstractmethod
    def visit_literal(self, element: Literal):
        pass  
    @abstractmethod
    def visit_group(self, element: Group):
        pass  
    @abstractmethod
    def visitExpressState(self, element: ExpressionState):
        pass  
    @abstractmethod
    def visitPrintState(self, element: PrintState):
        pass  
    

class ASTPrinter(Visitor):
    #I'm not gonna lie, I've had a lot of trouble getting the string to properly return so I don't know everything that is going on. 
    #First I create an data memebr string that can hold the important member data

    string = ""
    def visit_binary(self, element):
        #This visitor function has access to the expression functions and member data due to the accept method, then I pass the data member to teh parenthsize method
        return self.parenthesize(element.operator.lexeme, element.left, element.right)

    def visit_unary(self, element):
        #When I pass the member data to teh parenthesize method, I am able to print teh entire correct expression into the data member data
        return self.parenthesize(element.operator.lexeme, element.expre)
    
    def visit_group(self, element):
        #It is important to note that I am returning the string result of parenthesize. It least, that's what should be happening, but something isn't working.
        #As such, I am storing teh results of parenthesize in the member data and then printing that later. 
        return self.parenthesize(element.name, element.expre)

    def visit_literal(self, element):
        #Samne situation for this. 
        return self.parenthesize(element.value)
    
    #The Following code was inspired by kinshukk's Python implementation. I was really confused how to implement the method, forggetting that we are not printing 
    #and we are already overriding this method.
    def visitPrintState(self, element: PrintState):
        print("9")
        return None 
    def visitExpressState(self, element: ExpressionState):
        return None  

    def parenthesize(self, operatorr, *Expressions):
        #This method takes an whaT I AM CALLING AN OPERATOR and the following list of expressions. 
        #this allows me to pass the binary unary, or group member data to this method provided that I return the information with the operator first.
        #And as you can see in the code above, I do the same for the literal, but since there isn't no expressions, there shouldn't be any recursion happening. 
        self.string = f"({operatorr}"
        for Expression in Expressions:
            self.string += " ("
            self.string += Expression.__str__()
            self.string += ")"
        self.string += ")"
        return self.string

    def print(self, expres):
        #When we try to print We need to implement the accept method so that eventually the ASTPRINTER method can loop through the expression we provide. 
        return expres.accept(self)
'''
if __name__ == "__main__":
    #The following expression will be printed to teh terminal
    Expression = Binary(Unary(Token(TokenType.MINUS, 0, 0, '-', '-'), Literal(122) ), Token(TokenType.PLUS, 0, 0, '+', '+'), Group(Literal(5)))
    #First we instaiate an instance of a class. Then call the print method to help build the string needed to represent the expression above.
    #Then we need to print that expression. 
    print("This is the simplified expression:")
    visitor2 = ASTPrinter()
    visitor2.print(Expression)
    print(visitor2.string)
    
    '''
    