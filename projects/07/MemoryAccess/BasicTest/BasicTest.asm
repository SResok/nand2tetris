
            @10
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @0 // get which location
                D=A
                @LCL // variable
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

            
            @21
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
            @22
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @2 // get which location
                D=A
                @ARG // variable
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

            
                @1 // get which location
                D=A
                @ARG // variable
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

            
            @36
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @6 // get which location
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

            
            @42
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
            @45
            D=A
        
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                @5 // get which location
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

            
                @2 // get which location
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

            
            @510
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

                @11
                M=D
            
                    @0 
                    D=A 
                    @LCL 
                    D=D+M 
                    A=D 
                    D=M
            
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                    @5 
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
            
                    @1 
                    D=A 
                    @ARG 
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
                    @THIS 
                    D=D+M 
                    A=D 
                    D=M
            
            @SP 
            A=M 
            M=D

            @SP
            M=M+1
        
                    @6 
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
                M=M+D
            
                @SP
                M=M-1
                A=M
                D=M

                @SP
                A=M-1
                M=M-D
            
                @11
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
            