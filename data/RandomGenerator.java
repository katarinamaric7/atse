import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;

public class RandomGenerator {
    public static void generateArraysFile() {
        int arrayCount = 1000;
        Random rand = new Random();
        String fileName = "randomArrays.txt";

        try (PrintWriter writer = new PrintWriter(new FileWriter(fileName))) {
            for (int i = 0; i < arrayCount; i++) {
                int length = rand.nextInt(1000 - 10 + 1) + 10;
                
                for (int j = 0; j < length; j++) {
                    int num = rand.nextInt(100000) + 1;
                    
                    writer.print(num);
                    if (j < length - 1) {
                        writer.print(" ");
                    }
                }
                writer.println(); 
            }
            System.out.println("Successfully created '" + fileName + "' with " + arrayCount + " arrays in the current directory!");

        } catch (IOException e) {
            System.out.println("An error occurred while creating the file: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        generateArraysFile();
    }
}