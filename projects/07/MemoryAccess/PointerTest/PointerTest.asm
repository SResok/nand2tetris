
            @3030
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @SP
                M=M-1
                A=M
                D=M

                @THIS
                M=D
            
            @3040
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @SP
                M=M-1
                A=M
                D=M

                @THAT
                M=D
            
            @32
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @2 // get which location
                D=A
                @THIS // variable
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

            
            @46
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @6 // get which location
                D=A
                @THAT // variable
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

            
                @THIS
                D=M
                
                @SP 
                A=M 
                M=D

                @SP
                M=M+1
            
                @THAT
                D=M
                
                @SP 
                A=M 
                M=D

                @SP
                M=M+1
            
                @SP
                M=M-1
                A=M
                D=M

                @SP
                A=M-1
                M=M+D
            
                    @2 
                    D=A 
                    @THIS 
                    D=D+M 
                    A=D 
                    D=M
            
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @SP
                M=M-1
                A=M
                D=M

                @SP
                A=M-1
                M=M-D
            
                    @6 
                    D=A 
                    @THAT 
                    D=D+M 
                    A=D 
                    D=M
            
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @SP
                M=M-1
                A=M
                D=M

                @SP
                A=M-1
                M=M+D
            