import java.io.File;
import java.io.FileNotFoundException;


// Press Shift twice to open the Search Everywhere dialog and type `show whitespaces`,
// then press Enter. You can now see whitespace characters in your code.
public class VMTranslator {

    private final File inputFile;

    public static void main(String[] args) throws FileNotFoundException {

        File inputFile = null;
        if (args.length > 0) {
            inputFile = new File(args[0]);
        } else {
            System.err.println("Invalid arguments count:" + args.length);
            System.exit(0);
        }

        new VMTranslator( inputFile );
    }

    public VMTranslator(File inputFile) {
        this.inputFile = inputFile;

        new VMTranslator.Main();

    }

    class Main{
        private final String fileName;
        private final File outFile;


        public Main() {
            int index = VMTranslator.this.inputFile.getName().lastIndexOf(".");

            this.fileName = VMTranslator.this.inputFile.getName().substring(0,index);
            this.outFile = new File(VMTranslator.this.inputFile.getParent(), fileName + ".asm");


            Parser parser = new Parser(VMTranslator.this.inputFile);
            CodeWriter cw = new CodeWriter(this.fileName, this.outFile );
        }



    }

    class Parser{
        String[] commandTypes = {
                "C_ARITHMETIC",
                "C_PUSH",
                "C_POP",
                "C_LABEL",
                "C_GOTO",
                "C_IF",
                "C_FUNCTION",
                "C_RETURN",
                "C_CALL"
        };


        String[] currentCommand;
        String[] nextCommand;



        public Parser(File inputFile) {

        }



        public boolean hasMoreCommands(){
            return true;
        }

        public void advance(){

        }

        public String commandType(){
            return "";
        }

        public String arg1(){
            return "";
        }

        public int arg2(){
            return 0;
        }


    }

    class CodeWriter {
        private int label_no = 0;

        String gotoX = "@SP\n" + "A=M-1\n";
        String getXandGotoY = "@SP\n" + "AM=M-1\n" + "D=M\n" + "\n" + "A=A-1";

        public CodeWriter(String fileName, File outFile) {
            //open outfile


        }

        public void writeArithmetic(String command) {
            if (command == "not") {
//            gotoX + "M=!M";
            }
            if (command == "neg") {
//            gotoX + "M=-M"
            }

        }

        public void writePushPop(String command, String segment, int index) {

        }


        private void close() {

        }

        public String removeComments(String s) {
            return s.replaceAll("\\/\\* *\\w+ *\\*\\/", "");
        }
    }
}