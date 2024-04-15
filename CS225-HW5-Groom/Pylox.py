import Scanner
import Parser
import sys
import VisitorPattern
import interpreter
#At the top here we import sys so we can read arguments from the terminal,
# and we import scanner the scanner that imports the token and tokentype files, 
# giving us all the code we need to run the program

#Simply creating identifiers that are more similar to C++ syntactically because it is easier for me to read
argc = len(sys.argv)
args = sys.argv


    
class Pylox:
    def run_file(self, file_path):
        #Open file, read the contents of the file. Python is amazing since the identifier code here works as an array of chars
        #makes the code opens amd opens the file, then creates an array of chars code, 
        # then close the file and passes that array of chars to the begin scanning method. 
        file = open(file_path, 'r')
        code = file.read()
        file.close()
        #Essentially, the begin scanning method is used to create a scanner object,
        # scan the file, and print the results of the file
        self.begin_scanning(code)
        
        
        
        
    def run_REPL(self):
        #Enters prompt then waits for input, then will begin scanning the entered code until exit is inputed
        while True:
            line = input('>')
            if line == 'exit':
                break
            else:
                #Essentially, the begin scanning method is used to create a scanner object,
                # scan the file, and print the results of the file
                self.begin_scanning(line)
                
                
                
    def begin_scanning(self, code):
        #In the following code we build the an object Scanner and initialize it. 
        best_scanner = Scanner.Scanner(code, self)
        #Here we are storing the list of tokens in a variable list called tokens through
        # our scanner method that reads all the tokens in the file and returns that list
        tokens = best_scanner.scan_file()
        #Here we are simply fidning the length of our tokens list and using that length to loop through it. 
        tok_len = len(tokens)
        for x in range(tok_len):
            #Here we print the tokens from the tokens list that we recieved from the scan_file method 
            # #through referencing each token by their unique placement on the list
            print("[", end='')
            print(best_scanner.tokens[x].type, end='')
            print("]  Line: ", end='')
            print(best_scanner.tokens[x].line, end='')
            print(" Column: ", end='')
            print(best_scanner.tokens[x].column, end='')
            print(" Value: ", end='')
            print(best_scanner.tokens[x].literal)
            
        best_parser = Parser.Parser(tokens, self)
        statements = best_parser.parse()
        #These lines pass the expression to the ASTprinter to print it. 
        #printy = VisitorPattern.ASTPrinter()
        #answer = printy.print(statements)
        #print(answer)
        #Interprets the expression and prints it.
        interp = interpreter.Interpreter(self)
        interp.interpret(statements)

        
#here we are creating an instance of the pylox class so we can call its functions in main 
instance_of_pylox = Pylox()
if __name__ == '__main__': 
    #If there are more then two arguments then we have made a mistake because at most we
    # should only have two arguments, thus we exit.    
    if argc > 2:
        sys.exit(64)   
    elif argc == 2:
        #if we have two arguments, then the second one is the file we want so we pass
        # the path for the file to the run_file method
        instance_of_pylox.run_file(args[1])
    else:
        #If we just include the argument to run our program, then we will need to
        # create a REPL command line which need no arguments
        instance_of_pylox.run_REPL()
        
        