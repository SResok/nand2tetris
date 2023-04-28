import re
import sys
import os

class VMTranslator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.dir_path = os.path.dirname(input_file)
        self.file_name = os.path.splitext(os.path.basename(input_file))[0]
        self.out_file = os.path.join(self.dir_path, self.file_name + ".asm")
        
        self.reserved_variables = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
        self.translation = ""
        self.label_no = 0

    def remove_comments(self, string):
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

        def _replacer(match):
            if match.group(2) is not None:
                return ""
            else:
                return match.group(1)

        return regex.sub(_replacer, string)

    def handle_constant(self, value):
        return """
            @{0}
            D=A
        """.format(value) + self.handle_push()

    def handle_pointer(self, line):
        variable = "THIS" if line["value"] == 0 else "THAT"

        if line["action"] == "push":

            return """
                @{0}
                D=M
                
                @SP 
                A=M 
                M=D

                @SP
                M=M+1
            """.format( variable )

        elif line["action"] == "pop":
            
            return """
                @SP
                M=M-1
                A=M
                D=M

                @{0}
                M=D
            """.format( variable )
    
    def handle_segment(self, line):
        line = {
            "action": line[0],
            "segment": line[1],
            "value": int(line[2])
        }

        if line["segment"] in self.reserved_variables:
            return self.handle_reserved_variables(line)
        
        elif line["segment"] == "constant": # constant only pushes 
            return self.handle_constant(line["value"])
 
        elif line["segment"] == "static":
            return self.handle_static(line)

        elif line["segment"] == "temp":
            return self.handle_temp(line)

        elif line["segment"] == "pointer":
            return self.handle_pointer(line)

    def get_label(self):
        self.label_no += 1
        return self.label_no

    def handle_reserved_variables(self,line):
        variable = self.reserved_variables[line["segment"]]

        if line["action"] == "push":
            push = """
                    @{0} 
                    D=A 
                    @{1} 
                    D=D+M 
                    A=D 
                    D=M
            """.format(line["value"], variable)

            return push + self.handle_push()

        elif line["action"] == "pop":
            pop = """
                @{0} // get which location
                D=A
                @{1} // variable
                D=D+M // where to pop it

                @pop_temp_var // store chosen pop location in tmp variable
                M=D
                
                @SP // variable 
                M=M-1
                A=M
                D=M

                @pop_temp_var // pop it
                A=M
                M=D

            """.format( line["value"], variable )

            return pop




    def handle_temp(self, line):
        # temp 8 place segment
        # from 5 to 12

        temp_address = 5 + line["value"]

        if temp_address not in range(5, 12):
            sys.exit("temp error")

        if line["action"] == "push":
            push = """
                @{0}
                D=M
            """.format(temp_address) 

            return push + self.handle_push()

        elif line["action"] == "pop":
            return """                
                @SP
                M=M-1
                A=M
                D=M

                @{0}
                M=D
            """.format(temp_address)

    def handle_static(self, line):
        static_var = self.file_name + "." + str(line["value"])

        if line["action"] == "push":

            return """
            @{0}
            D=M
            
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
            """.format(static_var)

        elif line["action"] == "pop":
            
            return """
            @SP // variable 
            M=M-1
            A=M
            D=M

            @{0}
            M=D
        """.format(static_var)

    def handle_push(self):
        return """
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        """

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
        
    def translate(self):
        with open(self.input_file, 'r') as f:
            for line in f:
                line = self.remove_comments(line)
                if len(line) <= 1:
                    continue

                line = line.strip() and line.split()

                if len(line) == 1:  # math operation
                    self.translation += self.handle_operation(line[0])
                else:
                    segment = line[1]
                    if segment not in self.reserved_variables and segment not in ["constant","temp","pointer","static"]:
                        sys.exit("Unknown segment: {0}".format(segment))

                    self.translation += self.handle_segment(line)

        with open(self.out_file, 'w') as o:
            o.write(self.translation)

if not len(sys.argv) > 1: 
    sys.exit('no file provided, aborting...')
if not os.path.isfile(sys.argv[1]):
    sys.exit('file does not exist, aborting...')   

input_file = sys.argv[1]

VMTranslator(input_file).translate()