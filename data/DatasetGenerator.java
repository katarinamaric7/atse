import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedHashSet;
import java.util.Random;
import java.util.Set;

public class DatasetGenerator {

    private static final int VALUE_RANGE = 1_000_000;

    public static void main(String[] args) {


        int size = 100_000;
        if (args.length > 0) {
            size = Integer.parseInt(args[0]);
        }

        File dataDir = resolveDataDir();

        generateUniqueDataset(size, new File(dataDir, "big_datasets_unique_1_" + size + ".txt"));
        generateUniqueDataset(size, new File(dataDir, "big_datasets_unique_2_" + size + ".txt"));
    }

    public static void generateUniqueDataset(int size, File outFile) {

        int range = Math.max(VALUE_RANGE, size * 10);

        Random random = new Random();
        Set<Integer> values = new LinkedHashSet<>(); 

        while (values.size() < size) {
            values.add(random.nextInt(range));
        }

        outFile.getParentFile().mkdirs();

        try (FileWriter writer = new FileWriter(outFile)) {

            for (int value : values) {
                writer.write(value + "\n");
            }

            System.out.println("Created dataset (no duplicates) with " + size + " values:");
            System.out.println("  " + outFile.getAbsolutePath());

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    
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
