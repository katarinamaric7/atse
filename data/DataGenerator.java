import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class DataGenerator {

    // Fiksni seed da bi podaci uvek bili isti
    private static final Random random = new Random(42);

    // Broj različitih vrednosti (što je manji, više je duplikata)
    private static final int MAX_VALUE = 100;

    // Veličine datasetova
    private static final int[] SIZES = {
            1000,
            5000,
            10000,
            50000,
            100000
    };

    public static void main(String[] args) {

        createDatasetFolder();

        for (int size : SIZES) {
            generateDuplicateDataset(size);
        }

        System.out.println("Svi CSV fajlovi su uspešno generisani.");
    }

    /**
     * Kreira folder datasets ako ne postoji.
     */
    private static void createDatasetFolder() {

        File folder = new File("datasets");

        if (!folder.exists()) {
            folder.mkdir();
        }
    }

    /**
     * Generiše CSV fajl sa mnogo duplikata.
     */
    private static void generateDuplicateDataset(int size) {

        String fileName = "datasets/duplicates_" + size + ".csv";

        try (FileWriter writer = new FileWriter(fileName)) {

            for (int i = 0; i < size; i++) {

                int value = random.nextInt(MAX_VALUE);

                writer.write(String.valueOf(value));

                if (i != size - 1) {
                    writer.write(",");
                }
            }

            System.out.println(fileName + " napravljen.");

        } catch (IOException e) {
            System.out.println("Greška prilikom upisa u fajl:");
            e.printStackTrace();
        }
    }
}