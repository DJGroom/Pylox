
class Statement:
    pass
#

class PrintState(Statement):
    def __init__(self, expression):
        self.expression = expression
        #Since we want to use teh Visitor pattern to create a Abstract Syntax tree with the statements breaking down into expression.
        #We need to implement these Statements into the visitor method, which is actually quite easy, since all teh infrastructure is already here
        #kinshukk's python implementation helped me confirm that building an accept method was the correct way to go since the book didn't describe one
    def accept(self, visitor):
        return visitor.visitPrintState(self)
        
class ExpressionState(Statement):
    #For the member data, there is only the top expression for each statement, which will hold its own smaller abstract sytax tree. 
    def __init__(self, expression):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visitExpressState(self)