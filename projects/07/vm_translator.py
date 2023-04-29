import re
import sys
import os
from textwrap import dedent

class Parser(object):
    def remove_comments(self, string):
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

        def _replacer(match):
            if match.group(2) is not None:
                return ""
            else:
                return match.group(1)

        return regex.sub(_replacer, string)

    def get_commands(self, input_file):
        parsed_commands = []

        with open(input_file, 'r') as f:
            for command in f:
                command = self.remove_comments(command)
                if len(command) <= 1:
                    continue

                command = command.strip() and command.split()

                parsed_commands.append(command)

        return parsed_commands

class CodeWriter():
    def __init__(self, commands, file_name):
        self.file_name = file_name
        self.commands = commands

        self.command = []

        self.code = ""

        self.reserved_variables = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }

        self.label_no = 0

    def write(self):
        for i in range(len(self.commands)):
            self.handle_command(self.commands[i])

        return self.code

    
    def handle_command(self,command):
        self.code += "// " + " ".join(command)

        if len(command) == 1:  # math operation
            self.code += dedent(self.handle_operation(command[0]))
        else:
            segment = command[1]
            if segment not in self.reserved_variables and segment not in ["constant","temp","pointer","static"]:
                sys.exit("Unknown segment: {0}".format(segment))

            self.command = {
                "action": command[0],
                "segment": command[1],
                "value": int(command[2])
            }

            self.code += dedent(self.handle_segment(command[1]))

    def handle_operation(self, op):
        if op not in ["add", "sub", "eq","lt","gt","neg","and","not","or"]:
            sys.exit("Unknown operation: {0}".format(op))
        
        if op == "add":
            return """
                @SP
                AM=M-1
                D=M

                A=A-1
                M=M+D
            """

        elif op == "sub":
            return """
                @SP
                AM=M-1
                D=M

                A=A-1
                M=M-D
            """

        elif op == "eq":
            return """
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
        
        elif op == "lt":
            return """
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
            
        elif op == "gt":
            return """
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

        elif op == "neg":
            return """
                @SP
                A=M-1
                M=-M

            """
        
        elif op == "or":
            return """
                @SP
                AM=M-1
                D=M

                A=A-1
                D=D|M

                @SP
                A=M-1
                M=D
            """

        elif op == "not":
            return """
                @SP
                A=M-1
                M=!M
            """

        elif op == "and":
            return """
                @SP
                AM=M-1
                D=M

                A=A-1
                D=D&M

                @SP
                A=M-1
                M=D
            """
    def handle_segment(self, segment):
        if segment in self.reserved_variables:
            return self.handle_reserved_variables()
        
        elif segment == "constant":
            return self.handle_constant()
 
        elif segment == "static":
            return self.handle_static()

        elif segment == "temp":
            return self.handle_temp()

        elif segment == "pointer":
            return self.handle_pointer()

    def handle_reserved_variables(self):
        variable = self.reserved_variables[self.command["segment"]]

        if self.command["action"] == "push":
            push = """
            @{0} 
            D=A 
            @{1} 
            D=D+M 
            A=D 
            D=M
            """.format(self.command["value"], variable)

            return push + self.handle_push()

        elif self.command["action"] == "pop":
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

            """.format( self.command["value"], variable )

            return pop
    def handle_constant(self):
        return """
            @{0}
            D=A
        """.format(self.command["value"]) + self.handle_push()
    def handle_static(self):
        static_var = self.file_name + "." + str(line["value"])

        if self.command["action"] == "push":

            return """
            @{0}
            D=M
            
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
            """.format(static_var)

        elif self.command["action"] == "pop":
            
            return """
            @SP
            M=M-1
            A=M
            D=M

            @{0}
            M=D
        """.format(static_var)
    def handle_temp(self):
        # temp 8 place segment
        # from 5 to 12

        temp_address = 5 + self.command["value"]

        if temp_address not in range(5, 12):
            sys.exit("temp error")

        if self.command["action"] == "push":
            push = """
            @{0}
            D=M
            """.format(temp_address) 

            return push + self.handle_push()

        elif self.command["action"] == "pop":
            return """                
                @SP
                M=M-1
                A=M
                D=M

                @{0}
                M=D
            """.format(temp_address)
    def handle_pointer(self):
        variable = "THIS" if self.command["value"] == 0 else "THAT"

        if self.command["action"] == "push":

            return """
                @{0}
                D=M
                
                @SP 
                A=M 
                M=D

                @SP
                M=M+1
            """.format( variable )

        elif self.command["action"] == "pop":
            
            return """
                @SP
                M=M-1
                A=M
                D=M

                @{0}
                M=D
            """.format( variable ) 

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

class Main(object):
    def __init__(self, input_file):
        self.input_file = input_file
        self.file_name = os.path.splitext(os.path.basename(self.input_file))[0]
        
        self.translate()

    def translate(self):
        
        parser = Parser()
        parsed_commands = parser.get_commands(self.input_file)
        
        code_writer = CodeWriter(parsed_commands,self.file_name)
        translation = code_writer.write()

        # remove blank lines 
        translation = "\n".join([s for s in translation.split("\n") if s]) 

        dir_path = os.path.dirname(self.input_file)
        out_file = os.path.join(dir_path, self.file_name + ".asm")
        
        with open(out_file, 'w') as o:
            o.write(translation)





if not len(sys.argv) > 1: 
    sys.exit('no file provided, aborting...')
if not os.path.isfile(sys.argv[1]):
    sys.exit('file does not exist, aborting...')   

input_file = sys.argv[1]

Main(input_file)