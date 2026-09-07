import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.lang.management.ThreadMXBean;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import sort.SelectionSort;
import sort.MergeSort;
import sort.BubbleSort;
import sort.HeapSort;

public class Benchmark {

    @FunctionalInterface
    interface AlgorithmFunction {
        int[] run(int[] arr);
    }

    // null -> run every algorithm. A set -> run only those algo names.
    private static Set<String> selectedAlgos = null;

    public static void main(String[] args) {

        selectedAlgos = parseSelectedAlgos(args);
        if (selectedAlgos != null) {
            System.out.println("Running only: " + selectedAlgos);
        }

        File randomResultsDir =
                new File("../results/java/random");

        File duplicatesResultsDir =
                new File("../results/java/duplicates");

        File bigDataResultsDir =
                new File("../results/java/bigdata");

        createDirectory(randomResultsDir);
        createDirectory(duplicatesResultsDir);
        createDirectory(bigDataResultsDir);

        String[] allAlgoNames = {
                "SelectionSort",
                "ImprovedSelectionSort",
                "RecursiveMergeSort",
                "IterativeMergeSort",
                "BubbleSort",
                "BasicBubbleSort",
                "HeapSort",
                "RecursiveHeapSort"
        };

        String[] algoNames = filterAlgoNames(allAlgoNames);

        String randomFilePath =
                "../data/randomArrays.txt";

        System.out.println();
        System.out.println("############################################");
        System.out.println("#           RANDOM DATA TESTING            #");
        System.out.println("#                  3 RUNS                   #");
        System.out.println("############################################");

        prepareResultFiles(
                randomResultsDir,
                algoNames
        );

        processInputFile(
                randomFilePath,
                randomResultsDir,
                3
        );

        String[] duplicateFiles = {
                "../data/duplicates_1000.csv",
                "../data/duplicates_5000.csv",
                "../data/duplicates_10000.csv",
                "../data/duplicates_50000.csv"
        };

        System.out.println();
        System.out.println("############################################");
        System.out.println("#         DUPLICATES DATA TESTING          #");
        System.out.println("#                 30 RUNS                  #");
        System.out.println("############################################");

        prepareResultFiles(
                duplicatesResultsDir,
                algoNames
        );

        for (String duplicateFile : duplicateFiles) {

            System.out.println();
            System.out.println("============================================");
            System.out.println(
                    "TESTING FILE: " + duplicateFile
            );
            System.out.println("RUNS: 30");
            System.out.println("============================================");

            processInputFile(
                    duplicateFile,
                    duplicatesResultsDir,
                    30
            );
        }

        String[] bigDataFiles = {
                "../data/big_datasets_unique_1_100000.txt",
                "../data/big_datasets_unique_2_100000.txt"
        };

        System.out.println();
        System.out.println("############################################");
        System.out.println("#            BIG DATA TESTING              #");
        System.out.println("#                  30 RUNS                 #");
        System.out.println("#        EACH FILE = ONE BIG ARRAY         #");
        System.out.println("############################################");

        prepareResultFiles(
                bigDataResultsDir,
                algoNames
        );

        for (String bigDataFile : bigDataFiles) {

            System.out.println();
            System.out.println("============================================");
            System.out.println(
                    "TESTING BIG DATA FILE: " + bigDataFile
            );
            System.out.println("RUNS: 30");
            System.out.println("============================================");

            try {

                processBigDataFile(
                        bigDataFile,
                        bigDataResultsDir,
                        30
                );

            } catch (IOException e) {

                System.err.println(
                        "Greska pri citanju big data fajla: "
                                + bigDataFile
                );

                System.err.println(
                        e.getMessage()
                );
            }
        }

        System.out.println();
        System.out.println("############################################");
        System.out.println("#            TESTING FINISHED              #");
        System.out.println("############################################");

        System.out.println();
        System.out.println("Rezultati:");

        System.out.println(
                "../results/java/random/"
        );

        System.out.println(
                "../results/java/duplicates/"
        );

        System.out.println(
                "../results/java/bigdata/"
        );
    }

    /**
     * Reads the algorithm filter from the command line.
     * Returns null when no argument was given (= run everything).
     * Accepts full names ("BubbleSort") or shortcuts ("bubble", "heap",
     * "selection", "merge"), separated by spaces or commas.
     */
    private static Set<String> parseSelectedAlgos(String[] args) {

        if (args == null || args.length == 0) {
            return null;
        }

        Set<String> selected = new HashSet<>();

        for (String arg : args) {

            for (String token : arg.split("[,\\s]+")) {

                if (token.isEmpty()) {
                    continue;
                }

                switch (token.toLowerCase()) {
                    case "bubble":
                        selected.add("BubbleSort");
                        selected.add("BasicBubbleSort");
                        break;
                    case "heap":
                        selected.add("HeapSort");
                        selected.add("RecursiveHeapSort");
                        break;
                    case "selection":
                        selected.add("SelectionSort");
                        selected.add("ImprovedSelectionSort");
                        break;
                    case "merge":
                        selected.add("RecursiveMergeSort");
                        selected.add("IterativeMergeSort");
                        break;
                    default:
                        selected.add(token);
                }
            }
        }

        return selected;
    }

    /** Keeps only the algorithm names that pass the command-line filter. */
    private static String[] filterAlgoNames(String[] allAlgoNames) {

        if (selectedAlgos == null) {
            return allAlgoNames;
        }

        List<String> kept = new ArrayList<>();

        for (String name : allAlgoNames) {
            if (selectedAlgos.contains(name)) {
                kept.add(name);
            }
        }

        return kept.toArray(new String[0]);
    }

    private static void createDirectory(File directory) {

        if (!directory.exists()) {

            if (directory.mkdirs()) {

                System.out.println(
                        "Created directory: "
                                + directory.getPath()
                );

            } else {

                System.err.println(
                        "Could not create directory: "
                                + directory.getPath()
                );
            }
        }
    }

    private static void prepareResultFiles(
            File resultsDir,
            String[] algoNames) {

        for (String name : algoNames) {

            File resultFile =
                    new File(
                            resultsDir,
                            name + "Result.csv"
                    );

            if (resultFile.exists()) {

                if (!resultFile.delete()) {

                    System.err.println(
                            "Could not delete old result file: "
                                    + resultFile.getPath()
                    );
                }
            }

            try (BufferedWriter writer =
                         new BufferedWriter(
                                 new FileWriter(
                                         resultFile,
                                         true
                                 )
                         )) {

                writer.write(
                        "dataset,run,arraylength,time,cputime,memory"
                );

                writer.newLine();

            } catch (IOException e) {

                System.err.println(
                        "Greska pri kreiranju fajla za "
                                + name
                                + ": "
                                + e.getMessage()
                );
            }
        }
    }

    private static void processInputFile(
            String filePath,
            File resultsDir,
            int numberOfRuns) {

        String datasetName =
                new File(filePath).getName();

        int dotIndex =
                datasetName.lastIndexOf('.');

        if (dotIndex > 0) {

            datasetName =
                    datasetName.substring(
                            0,
                            dotIndex
                    );
        }

        for (int run = 1; run <= numberOfRuns; run++) {

            System.out.println();
            System.out.println(
                    "============================================"
            );

            System.out.println(
                    "Dataset: " + datasetName
            );

            System.out.println(
                    "Run: " + run + "/" + numberOfRuns
            );

            System.out.println(
                    "============================================"
            );

            try {

                List<int[]> arrays =
                        readArraysFromFile(filePath);

                int arrayCounter = 1;

                for (int[] originalArr : arrays) {

                    System.out.println(
                            "=== RUN #" + run
                                    + " | ARRAY #" + arrayCounter
                                    + " | Length: "
                                    + originalArr.length
                                    + " ==="
                    );

                    measureAndSave(
                            datasetName,
                            run,
                            "SelectionSort",
                            originalArr,
                            resultsDir,
                            arr -> {

                                SelectionSort.selection_sort(arr);

                                return arr;
                            }
                    );

                    measureAndSave(
                            datasetName,
                            run,
                            "ImprovedSelectionSort",
                            originalArr,
                            resultsDir,
                            arr -> {

                                SelectionSort.improved_selection_sort(arr);

                                return arr;
                            }
                    );

                    measureAndSave(
                            datasetName,
                            run,
                            "RecursiveMergeSort",
                            originalArr,
                            resultsDir,
                            arr ->
                                    MergeSort.mergeSort(arr)
                    );

                    measureAndSave(
                            datasetName,
                            run,
                            "IterativeMergeSort",
                            originalArr,
                            resultsDir,
                            arr ->
                                    MergeSort.mergeSortWithoutRecursion(arr)
                    );

                    measureAndSave(
                            datasetName,
                            run,
                            "BubbleSort",
                            originalArr,
                            resultsDir,
                            arr -> {

                                BubbleSort.sort(arr);

                                return arr;
                            }
                    );

                    measureAndSave(
                            datasetName,
                            run,
                            "BasicBubbleSort",
                            originalArr,
                            resultsDir,
                            arr -> {

                                BubbleSort.sortBasic(arr);

                                return arr;
                            }
                    );

                    measureAndSave(
                            datasetName,
                            run,
                            "HeapSort",
                            originalArr,
                            resultsDir,
                            arr -> {

                                HeapSort.sort(arr);

                                return arr;
                            }
                    );

                    measureAndSave(
                            datasetName,
                            run,
                            "RecursiveHeapSort",
                            originalArr,
                            resultsDir,
                            arr -> {

                                HeapSort.sortRecursive(arr);

                                return arr;
                            }
                    );

                    System.out.println(
                            "--------------------------------------------"
                    );

                    arrayCounter++;
                }

            } catch (IOException e) {

                System.out.println(
                        "Error: The file '"
                                + filePath
                                + "' does not exist!"
                );

                System.out.println(
                        "Please check the data directory."
                );
            }
        }
    }

    private static void processBigDataFile(
            String filePath,
            File resultsDir,
            int numberOfRuns) throws IOException {

        String datasetName =
                new File(filePath).getName();

        int dotIndex =
                datasetName.lastIndexOf('.');

        if (dotIndex > 0) {

            datasetName =
                    datasetName.substring(
                            0,
                            dotIndex
                    );
        }

        int[] originalArr =
                readBigDataFile(filePath);

        System.out.println();
        System.out.println(
                "Dataset: " + datasetName
        );

        System.out.println(
                "Array length: "
                        + originalArr.length
        );

        for (int run = 1; run <= numberOfRuns; run++) {

            System.out.println();
            System.out.println(
                    "============================================"
            );

            System.out.println(
                    "Dataset: " + datasetName
            );

            System.out.println(
                    "Run: " + run + "/" + numberOfRuns
            );

            System.out.println(
                    "Array length: "
                            + originalArr.length
            );

            System.out.println(
                    "============================================"
            );

            measureAndSave(
                    datasetName,
                    run,
                    "SelectionSort",
                    originalArr,
                    resultsDir,
                    arr -> {

                        SelectionSort.selection_sort(arr);

                        return arr;
                    }
            );

            measureAndSave(
                    datasetName,
                    run,
                    "ImprovedSelectionSort",
                    originalArr,
                    resultsDir,
                    arr -> {

                        SelectionSort.improved_selection_sort(arr);

                        return arr;
                    }
            );

            measureAndSave(
                    datasetName,
                    run,
                    "RecursiveMergeSort",
                    originalArr,
                    resultsDir,
                    arr ->
                            MergeSort.mergeSort(arr)
            );

            measureAndSave(
                    datasetName,
                    run,
                    "IterativeMergeSort",
                    originalArr,
                    resultsDir,
                    arr ->
                            MergeSort.mergeSortWithoutRecursion(arr)
            );

            measureAndSave(
                    datasetName,
                    run,
                    "BubbleSort",
                    originalArr,
                    resultsDir,
                    arr -> {

                        BubbleSort.sort(arr);

                        return arr;
                    }
            );

            measureAndSave(
                    datasetName,
                    run,
                    "BasicBubbleSort",
                    originalArr,
                    resultsDir,
                    arr -> {

                        BubbleSort.sortBasic(arr);

                        return arr;
                    }
            );

            measureAndSave(
                    datasetName,
                    run,
                    "HeapSort",
                    originalArr,
                    resultsDir,
                    arr -> {

                        HeapSort.sort(arr);

                        return arr;
                    }
            );

            measureAndSave(
                    datasetName,
                    run,
                    "RecursiveHeapSort",
                    originalArr,
                    resultsDir,
                    arr -> {

                        HeapSort.sortRecursive(arr);

                        return arr;
                    }
            );

            System.out.println(
                    "--------------------------------------------"
            );
        }
    }

    private static List<int[]> readArraysFromFile(
            String filePath) throws IOException {

        List<int[]> arrays =
                new ArrayList<>();

        try (BufferedReader br =
                     new BufferedReader(
                             new FileReader(filePath)
                     )) {

            String line;

            while ((line = br.readLine()) != null) {

                line = line.trim();

                if (line.isEmpty()) {
                    continue;
                }

                String[] tokens =
                        line.split("[,\\s]+");

                int[] arr =
                        new int[tokens.length];

                boolean validLine = true;

                for (int i = 0; i < tokens.length; i++) {

                    try {

                        arr[i] =
                                Integer.parseInt(
                                        tokens[i].trim()
                                );

                    } catch (NumberFormatException e) {

                        validLine = false;

                        System.err.println(
                                "Preskacem nevalidan red: "
                                        + line
                        );

                        break;
                    }
                }

                if (validLine && arr.length > 0) {

                    arrays.add(arr);
                }
            }
        }

        return arrays;
    }

    private static int[] readBigDataFile(
            String filePath) throws IOException {

        List<Integer> numbers =
                new ArrayList<>();

        try (BufferedReader br =
                     new BufferedReader(
                             new FileReader(filePath)
                     )) {

            String line;

            while ((line = br.readLine()) != null) {

                line = line.trim();

                if (line.isEmpty()) {
                    continue;
                }

                String[] tokens =
                        line.split("[,\\s]+");

                for (String token : tokens) {

                    if (!token.isEmpty()) {

                        numbers.add(
                                Integer.parseInt(
                                        token.trim()
                                )
                        );
                    }
                }
            }
        }

        int[] array =
                new int[numbers.size()];

        for (int i = 0; i < numbers.size(); i++) {

            array[i] =
                    numbers.get(i);
        }

        return array;
    }

    private static void measureAndSave(
            String datasetName,
            int run,
            String algoName,
            int[] originalArr,
            File resultsDir,
            AlgorithmFunction algo) {

        if (selectedAlgos != null && !selectedAlgos.contains(algoName)) {
            return;
        }

        int[] arrCopy =
                Arrays.copyOf(
                        originalArr,
                        originalArr.length
                );

        ThreadMXBean threadBean =
                ManagementFactory.getThreadMXBean();

        System.gc();

        try {

            Thread.sleep(10);

        } catch (InterruptedException ignored) {
        }

        Runtime runtime =
                Runtime.getRuntime();

        long memBefore =
                runtime.totalMemory()
                        - runtime.freeMemory();

        long startWallTime =
                System.nanoTime();

        long startCpuTime =
                threadBean.isCurrentThreadCpuTimeSupported()
                        ? threadBean.getCurrentThreadCpuTime()
                        : 0;

        int[] sortedArr =
                algo.run(arrCopy);

        long endCpuTime =
                threadBean.isCurrentThreadCpuTimeSupported()
                        ? threadBean.getCurrentThreadCpuTime()
                        : 0;

        long endWallTime =
                System.nanoTime();

        long memAfter =
                runtime.totalMemory()
                        - runtime.freeMemory();

        double wallTimeMs =
                (endWallTime - startWallTime)
                        / 1_000_000.0;

        double cpuTimeMs =
                (endCpuTime - startCpuTime)
                        / 1_000_000.0;

        double memoryUsedKb =
                Math.max(
                        0,
                        (memAfter - memBefore)
                                / 1024.0
                );

        System.out.print(
                "  [" + algoName + "] (first 10): "
        );

        printFirstTen(sortedArr);

        System.out.printf(
                "    -> Time: %.2f ms"
                        + " | CPU Time: %.2f ms"
                        + " | Memory: %.2f KB%n",
                wallTimeMs,
                cpuTimeMs,
                memoryUsedKb
        );

        File resultFile =
                new File(
                        resultsDir,
                        algoName + "Result.csv"
                );

        try (BufferedWriter writer =
                     new BufferedWriter(
                             new FileWriter(
                                     resultFile,
                                     true
                             )
                     )) {

            writer.write(
                    String.format(
                            "%s,%d,%d,%.2f,%.2f,%.2f",
                            datasetName,
                            run,
                            originalArr.length,
                            wallTimeMs,
                            cpuTimeMs,
                            memoryUsedKb
                    )
            );

            writer.newLine();

        } catch (IOException e) {

            System.err.println(
                    "Greska pri upisu rezultata za "
                            + algoName
                            + ": "
                            + e.getMessage()
            );
        }
    }

    private static void printFirstTen(int[] arr) {

        int limit =
                Math.min(
                        10,
                        arr.length
                );

        int[] firstTen =
                Arrays.copyOfRange(
                        arr,
                        0,
                        limit
                );

        System.out.println(
                Arrays.toString(firstTen)
        );
    }
}
