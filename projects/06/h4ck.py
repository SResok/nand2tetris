import re, sys

inFile = sys.argv[1]
outFile = sys.argv[2]

# # f = open("./max/Max.asm", "r")

# f = open("./rect/Rect.asm", "r")

dedicatedAdress = {
    "SCREEN": 16384,
    "KBD": 24576,
    "SP":0,
    "LCL": 1,
    "ARG":2,
    "THIS":3,
    "THAT":4
}
for i in range(16):
    dedicatedAdress["R" + str(i)] = i 

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

jump = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

dest = {
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

# first pass
currentLine = 0
labels_stripped = ""

with open(inFile,'r') as f:
    for line in f:
        line = remove_comments(line)
        
        if len(line) > 1:
            line = line.strip()
            
            if match := re.search(r'^\((\D.*)\)', line): ##################### store label(adress) and skip adding as line
                dedicatedAdress[match.group(1)] = currentLine # @LABEL = currentLine
                continue # skip adding line

            currentLine += 1
            labels_stripped += line + "\n"

freeAddress = 16
final = ""

for line in labels_stripped.splitlines():
    if match := re.search(r'^@(\D.*)|^@(\d.*)', line): # replace symbols > A instruction
        
        if match.group(1): # if is label
            line = match.group(1) # line = label

            if line in dedicatedAdress :
                    line = bin(dedicatedAdress[line])
            else:
                dedicatedAdress[line] = freeAddress
                line = bin(freeAddress)
                freeAddress += 1

        elif match.group(2): 
            line = bin(int(match.group(2))) # line = int

        line = line[2:] # strip bin() '0b'

        instruction = "0000000000000000"[:-len(line)] + line # remove length of line from 16 bit instruction and add line itself
    
    else: # C instruction
        comp_bits = "0000000"
        dest_bits = "000"
        jump_bits = "000"

        if match := re.search(r'^(.+)=(.*)', line): # comp XXX = XXX
            dest_bits = dest[match.group(1)]
            comp_bits = comp[match.group(2)]

        if match := re.search(r'^(.+);.*', line): # XXX ; XXX
            comp_bits = comp[match.group(1)]

        if match := re.search(r'^.+;([A-Z]{3})', line): # jump
            jump_bits = jump[match.group(1)]


        instruction = "111" + comp_bits + dest_bits + jump_bits
        
    final += instruction + "\n"
    
with open(outFile,'w') as o:
    # o.write(final.rstrip())
    o.write(final)


        
    