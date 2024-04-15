import Scanner
#Code was inspired from JHonaker's interpretation of the interpreter for Python
#I didn't write a couple methods like IsTruthy and IsEqual beacuse I found work arounds
#It is important to note this overriding the methods is already happening here, so we implement these methods instead the methods
#inthe VisitorPattern. 
class Interpreter:
    def __init__(self, pylox):
        self.pylox = pylox
        #Here we pass ourselves to the interpreter class


    def interpret(self, statements):
        #here we call we evaluate the expression, creating a recursive cycle that will return the final results 
        #of the Abstract Syntax Tree
        for Statement in statements:
            self.execute(Statement)
            
        
        #results = self.execute(statements)
        #Then we turn those results to a string and return that string to Pylox to be printed. 
        #answer = self.stringify(results)
        #return answer
        
    def execute(self, statement):
        #there is no difference between the two methods, it is only a meaning difference
        return statement.accept(self)
    def evaluate(self, expression):
        #though technically we don't evaluate statements we execute them, this function can be used for statments 
        #as well due to Python's typing
        ## We are working under the assumption that we already have used the visitor pattern to represnt our string.
        return expression.accept(self)

    def visit_literal(self, expression):
        #here we simply 
        return expression.value

    def stringify(self, results):
        #Stringify is very easy in Python, we just call the built-in str() method that prints the appropreiate string 
        #that even works with True and False.
        if results is None:
            return "nil"
        else:
            return str(results)
    
    def visitExpressState(self, exstatement):
        self.evaluate(exstatement.expression)
        return None
    def visitPrintState(self, pstatement):
        results = self.evaluate(pstatement.expression)
        print(self.stringify(results))
        return None

    def visit_binary(self, expression):
        # the following code will begin a recursive cycle down the abstract syntax tree of the expression. 
        #When at the down of teh tree, we will return the result the binary to the previous unary, binary, or group. 
        #Thus beginning the recursive cycle again till we reach the top of the syntax tree where we have the final result
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)
        if(right == None):
            right = False
        if(left == None):
            left = False

        token = expression.operator.type
        #The following code compares the token in the binary to see what type of operation needs to be done on 
        #the results of teh expressions
        match token:
            case Scanner.TokenType.STAR:
                return (left * right)
            case Scanner.TokenType.SLASH:
                if(right == 0):
                    #Can't divide by zero so I have it return zero.
                    right = 1
                    left = 0
                return (left / right)
            case Scanner.TokenType.MINUS:
                return (left - right)
            case Scanner.TokenType.PLUS:
                #The string adding is weird. If you put "hello" + "world" it prints the string "hello""world"
                #I am a bit confused how exactly to solve this problem. 
                if isinstance(left, str) & isinstance(right, str):
                    return (left + right)
                else:
                    return (left + right)
            case Scanner.TokenType.GREATER:
                return (left > right)
            case Scanner.TokenType.LESS:
                return (left < right)
            case Scanner.TokenType.GREATER_EQUAL:
                return (left >= right)
            case Scanner.TokenType.LESS_EQUAL:
                return (left <= right)
            case Scanner.TokenType.EQUAL_EQUAL:
                return (left == right)
            case Scanner.TokenType.BANG_EQUAL:
                return (left != right)

        return None

    def visit_unary(self, expression):
        #first we must evaluate the expression inside to get a  value
        #if that value is a number we simply 
        right = self.evaluate(expression.expre)
        
        if(expression.operator.type == Scanner.TokenType.MINUS):
            return (-1 * right)
        if(expression.operator.type == Scanner.TokenType.BANG):
            if right is True:
                return False
            if right is False:
                return True
            else:
                return None
        #Something is weird with this part of the method and it won't work, needs further work
        
    def visit_group(self, expression):
        #Group is really quite simply, we just evaluate the expression inside. Following the recursive nature or teh AST
        return self.evaluate(expression.expre)
        