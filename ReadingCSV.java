import java.util.Scanner;
import java.io.File;
import java.io.IOException;

public class ReadingCSV {
    public static void main(String args[]) throws IOException {
        Scanner in = new Scanner(new File("/Users/kunal/Documents/Internship/Data.csv"));
        in.useDelimiter(",");
        // Used to skip over strings which contain digits
        String pattern = ".*[1-9].*";
        while (in.hasNext()) {
            System.out.println(in.next());
            in.skip(pattern);
        }
    }
}