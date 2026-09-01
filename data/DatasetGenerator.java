import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class DatasetGenerator {

    public static void main(String[] args) {

        // Default size, or pass a number as the first argument: java DatasetGenerator 1000000
        int size = 100_000;
        if (args.length > 0) {
            size = Integer.parseInt(args[0]);
        }

        File outFile = new File(resolveDataDir(), "big_datasets_" + size + ".txt");
        generateDataset(size, outFile);
    }

    public static void generateDataset(int size, File outFile) {

        Random random = new Random();
        outFile.getParentFile().mkdirs();

        try (FileWriter writer = new FileWriter(outFile)) {

            for (int i = 0; i < size; i++) {

                // range values (0 - 1.000.000)
                int value = random.nextInt(1_000_000);

                writer.write(value + "\n");
            }

            System.out.println("Created dataset with " + size + " values:");
            System.out.println("  " + outFile.getAbsolutePath());

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Finds the atse/data folder no matter which working directory the program
     * is started from (project root, atse/, or atse/data/). Falls back to a
     * "data" folder under the current directory.
     */
    private static File resolveDataDir() {
        File dir = new File("").getAbsoluteFile();

        while (dir != null) {
            File candidate = new File(dir, "atse/data");
            if (candidate.isDirectory()) {
                return candidate;
            }
            if (dir.getName().equals("data") && new File(dir.getParentFile(), "data").isDirectory()) {
                return dir;
            }
            dir = dir.getParentFile();
        }

        return new File("data");
    }
}
