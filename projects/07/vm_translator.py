import re
import sys
import os
from textwrap import dedent


class Main:
    def __init__(self, input_file):
        input_file = input_file
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        dir_path = os.path.dirname(input_file)
        out_file = os.path.join(dir_path, file_name + ".asm")
        
        self.parser = Parser(input_file)
        self.code_writer = CodeWriter(file_name, out_file)


    def translate(self):

        self.parser.get_next_command()
        self.parser.advance()
        
        while self.parser.current_command:
            self.code_writer.write("// {0}".format(" ".join(self.parser.current_command)))
            if self.parser.get_command_type() == self.parser.types["arithmetic"]:
                self.code_writer.write_arithmetic(self.parser.arg1())
            elif self.parser.get_command_type() in ["C_PUSH","C_POP"]:
                self.code_writer.write_push_pop(self.parser.get_command_type(), self.parser.arg1(), self.parser.arg2())

            self.parser.advance()

        # # remove blank lines 
        # translation = "\n".join([s for s in translation.split("\n") if s]) 

class Parser:
    def __init__(self, input_file):
        self.types = {
            "arithmetic": "C_ARITHMETIC",
            "push":"C_PUSH",
            "pop": "C_POP",
            "label":"C_LABEL",
            "goto": "C_GOTO",
            "if":"C_IF",
            "function":"C_FUNCTION",
            "return":"C_RETURN",
            "call": "C_CALL"
        }
        
        self.input_file = open(input_file, 'r')

        self.current_command = None
        self.next_command = None

    def remove_comments(self, string):
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

        def _replacer(match):
            if match.group(2) is not None:
                return ""
            else:
                return match.group(1)

        return regex.sub(_replacer, string)
    
    def get_command_type(self):
        if len(self.current_command) == 1:
            return self.types["arithmetic"]

        if self.current_command[0] not in self.types:
            sys.exit("Unknown types: {0}".format(current_command[1]))

        else:
            return self.types[self.current_command[0]]
    
    
    def advance(self):
        self.current_command = self.next_command
        self.get_next_command()

    def get_next_command(self):
        if self.next_command == False: ### last command to parse
            self.current_command = self.next_command
            return

        line = self.input_file.readline()

        if not line:
            self.close()
            self.next_command = False
            return
        
        line = self.remove_comments(line)
        if len(line) <= 1:
            self.get_next_command()
            return
        
        self.next_command = line.strip() and line.split()

    def has_more_commands(self):
        return True if self.next_command else False


    def arg1(self):
        if self.get_command_type() == self.types["arithmetic"]:
            return self.current_command[0]
        
        if self.current_command == self.types["return"]:
            sys.exit("Should not be called from: {0}".format(self.types["return"]))

        else: return self.current_command[1]


    def arg2(self):
        for allowed in ["push","pop","function","call"]:
            if self.get_command_type() == self.types[allowed]:
                return int(self.current_command[2])

    def close(self):
        self.input_file.close()

class CodeWriter:
    def __init__(self, file_name, out_file):
        self.file_name = file_name
        self.reserved_variables = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }

        self.label_no = 0        

        self.out_file = open(out_file, 'w')

    def write_arithmetic(self,command):
        if command not in ["add", "sub", "eq","lt","gt","neg","and","not","or"]:
            sys.exit("Unknown operation: {0}".format(command))

        code = ""

        if command == "add":
            code = """
                @SP
                AM=M-1
                D=M

                A=A-1
                M=M+D
            """

        elif command == "sub":
            code = """
                @SP
                AM=M-1
                D=M

                A=A-1
                M=M-D
            """

        elif command == "eq":
            code = """
                @SP
                AM=M-1
                D=M

                A=A-1
                D=M-D

                @OP{0}
                D;JEQ
                
                @SP
                A=M-1
                M=0

                @END{0}
                0;JMP

                (OP{0})
                @SP
                A=M-1
                M=-1

                (END{0})
            """.format(self.get_label())
        
        elif command == "lt":
            code = """
                @SP
                AM=M-1
                D=M

                A=A-1
                D=M-D

                @OP{0}
                D;JLT
                
                @SP
                A=M-1
                M=0

                @END{0}
                0;JMP

                (OP{0})
                @SP
                A=M-1
                M=-1
                    
                (END{0})
            """.format(self.get_label())
            
        elif command == "gt":
            code = """
                @SP
                AM=M-1
                D=M

                A=A-1
                D=M-D

                @OP{0}
                D;JGT
                
                @SP
                A=M-1
                M=0

                @END{0}
                0;JMP

                (OP{0})
                @SP
                A=M-1
                M=-1

                (END{0})
            """.format(self.get_label())

        elif command == "neg":
            code = """
                @SP
                A=M-1
                M=-M
            """
        
        elif command == "or":
            code = """
                @SP
                AM=M-1
                D=M

                A=A-1
                D=D|M

                @SP
                A=M-1
                M=D
            """

        elif command == "not":
            code = """
                @SP
                A=M-1
                M=!M
            """

        elif command == "and":
            code = """
                @SP
                AM=M-1
                D=M

                A=A-1
                D=D&M

                @SP
                A=M-1
                M=D
            """

        self.write(code)

    def write_push_pop(self, action, segment, value):
        if segment not in self.reserved_variables and segment not in ["constant","temp","pointer","static"]:
            sys.exit("Unknown segment: {0}".format(segment))
        print(value)
        if action == "C_PUSH":
            if segment in self.reserved_variables:
                variable = self.reserved_variables[segment]
                self.write("""
                @{0} 
                D=A 
                @{1} 
                D=D+M 
                A=D 
                D=M
                """.format(value, variable) + self.handle_push())
            if segment == "constant":
                self.write("""
                @{0}
                D=A
                """.format(value) + self.handle_push())
            elif segment == "static":
                static_var = self.file_name + "." + str(value)
                self.write("""
                @{0}
                D=M
                
                @SP 
                A=M 
                M=D

                @SP
                M=M+1
                """.format(static_var))
            elif segment == "temp":
                temp_address = 5 + value

                if temp_address not in range(5, 12):
                    sys.exit("temp error")

                push = """
                @{0}
                D=M
                """.format(temp_address) 

                self.write(push + self.handle_push())                
            elif segment == "pointer":
                variable = "THIS" if value == 0 else "THAT"
                self.write("""
                    @{0}
                    D=M
                    
                    @SP 
                    A=M 
                    M=D

                    @SP
                    M=M+1
                """.format( variable ))

        elif action == "C_POP":
            if segment in self.reserved_variables:
                variable = self.reserved_variables[segment]
                pop = """
                @{0}
                D=A
                @{1}
                D=D+M 

                @pop_temp_var
                M=D
                
                @SP
                M=M-1
                A=M
                D=M

                @pop_temp_var
                A=M
                M=D

                """.format( value, variable )

                self.write(pop)
            elif segment == "static":
                static_var = self.file_name + "." + str(value)
                self.write("""
                    @SP
                    M=M-1
                    A=M
                    D=M

                    @{0}
                    M=D
                """.format(static_var))
            elif segment == "temp":
                temp_address = 5 + value

                if temp_address not in range(5, 12):
                    sys.exit("temp error")

                self.write("""                
                    @SP
                    M=M-1
                    A=M
                    D=M

                    @{0}
                    M=D
                """.format(temp_address))            
            elif segment == "pointer":
                variable = "THIS" if value == 0 else "THAT"
                self.write("""
                @SP
                M=M-1
                A=M
                D=M

                @{0}
                M=D
                """.format( variable ) )


    def write(self, code):
        self.out_file.write(code)    
    def close(self):
        self.out_file.close()

    def get_label(self):
        self.label_no += 1
        return self.label_no
    def handle_push(self):
        return """
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        """
    





if not len(sys.argv) > 1: 
    sys.exit('no file provided, aborting...')
if not os.path.isfile(sys.argv[1]):
    sys.exit('file does not exist, aborting...')   

input_file = sys.argv[1]

vm_translator = Main(input_file)
vm_translator.translate()