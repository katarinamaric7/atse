import csv
import os
import sys
import time
import psutil

from sort.SelectionSort import SelectionSort
from sort.MergeSort import MergeSort
from sort.BubbleSort import BubbleSort
from sort.HeapSort import HeapSort


# None -> run every algorithm. A set -> run only those algo_name values.
SELECTED_ALGOS = None

# Friendly shortcuts you can pass on the command line instead of full names.
ALGO_ALIASES = {
    "bubble": ["BubbleSort", "BasicBubbleSort"],
    "heap": ["HeapSort", "RecursiveHeapSort"],
    "selection": ["SelectionSort", "ImprovedSelectionSort"],
    "merge": ["RecursiveMergeSort", "IterativeMergeSort"],
}


def parse_selected_algos(args):
    if not args:
        return None
    tokens = " ".join(args).replace(",", " ").split()
    selected = set()
    for token in tokens:
        key = token.lower()
        if key in ALGO_ALIASES:
            selected.update(ALGO_ALIASES[key])
        else:
            selected.add(token)
    return selected


def main():

    global SELECTED_ALGOS
    SELECTED_ALGOS = parse_selected_algos(sys.argv[1:])
    if SELECTED_ALGOS is not None:
        print("Running only: " + ", ".join(sorted(SELECTED_ALGOS)))

    random_results_dir = "../results/python/random"
    duplicates_results_dir = "../results/python/duplicates"
    big_data_results_dir = "../results/python/bigdata"

    create_directory(random_results_dir)
    create_directory(duplicates_results_dir)
    create_directory(big_data_results_dir)

    algo_names = [
        "SelectionSort",
        "ImprovedSelectionSort",
        "RecursiveMergeSort",
        "IterativeMergeSort",
        "BubbleSort",
        "BasicBubbleSort",
        "HeapSort",
        "RecursiveHeapSort"
    ]

    if SELECTED_ALGOS is not None:
        algo_names = [
            name for name in algo_names if name in SELECTED_ALGOS
        ]

    random_file_path = "../data/randomArrays.txt"

    print()
    print("############################################")
    print("#           RANDOM DATA TESTING            #")
    print("#                  3 RUNS                   #")
    print("############################################")

    prepare_result_files(
        random_results_dir,
        algo_names
    )

    process_input_file(
        random_file_path,
        random_results_dir,
        3
    )

    duplicate_files = [
        "../data/duplicates_1000.csv",
        "../data/duplicates_5000.csv",
        "../data/duplicates_10000.csv",
        "../data/duplicates_50000.csv"
    ]

    print()
    print("############################################")
    print("#         DUPLICATES DATA TESTING          #")
    print("#        30 RUNS / 50000 = 2 RUNS          #")
    print("############################################")

    prepare_result_files(
        duplicates_results_dir,
        algo_names
    )

    for duplicate_file in duplicate_files:

        if "duplicates_50000" in duplicate_file:
            number_of_runs = 2
        else:
            number_of_runs = 30

        print()
        print("============================================")
        print("TESTING FILE: " + duplicate_file)
        print("RUNS: " + str(number_of_runs))
        print("============================================")

        process_input_file(
            duplicate_file,
            duplicates_results_dir,
            number_of_runs
        )

    big_data_files = [
        "../data/big_datasets_unique_1_100000.txt",
        "../data/big_datasets_unique_2_100000.txt"
    ]

    print()
    print("############################################")
    print("#            BIG DATA TESTING              #")
    print("#                  1 RUN                   #")
    print("#        EACH FILE = ONE BIG ARRAY         #")
    print("############################################")

    prepare_result_files(
        big_data_results_dir,
        algo_names
    )

    for big_data_file in big_data_files:

        print()
        print("============================================")
        print("TESTING BIG DATA FILE: " + big_data_file)
        print("RUNS: 1")
        print("============================================")

        try:

            process_big_data_file(
                big_data_file,
                big_data_results_dir,
                1
            )

        except (OSError, ValueError) as e:

            print(
                "Greska pri citanju big data fajla: "
                + big_data_file
            )

            print(str(e))

    print()
    print("############################################")
    print("#            TESTING FINISHED              #")
    print("############################################")

    print()
    print("Rezultati:")

    print("../results/python/random/")
    print("../results/python/duplicates/")
    print("../results/python/bigdata/")


def create_directory(directory):

    if not os.path.exists(directory):

        try:

            os.makedirs(directory)

            print(
                "Created directory: "
                + directory
            )

        except OSError:

            print(
                "Could not create directory: "
                + directory
            )


def prepare_result_files(results_dir, algo_names):

    for name in algo_names:

        result_file = os.path.join(
            results_dir,
            name + "Result.csv"
        )

        if os.path.exists(result_file):

            try:

                os.remove(result_file)

            except OSError:

                print(
                    "Could not delete old result file: "
                    + result_file
                )

        try:

            with open(
                result_file,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "dataset",
                    "run",
                    "arraylength",
                    "time",
                    "cputime",
                    "memory"
                ])

        except OSError as e:

            print(
                "Greska pri kreiranju fajla za "
                + name
                + ": "
                + str(e)
            )


def process_input_file(
        file_path,
        results_dir,
        number_of_runs):

    dataset_name = os.path.basename(file_path)

    dataset_name = os.path.splitext(
        dataset_name
    )[0]

    for run in range(1, number_of_runs + 1):

        print()
        print(
            "============================================"
        )

        print(
            "Dataset: " + dataset_name
        )

        print(
            "Run: "
            + str(run)
            + "/"
            + str(number_of_runs)
        )

        print(
            "============================================"
        )

        try:

            arrays = read_arrays_from_file(
                file_path
            )

            array_counter = 1

            for original_arr in arrays:

                print(
                    "=== RUN #"
                    + str(run)
                    + " | ARRAY #"
                    + str(array_counter)
                    + " | Length: "
                    + str(len(original_arr))
                    + " ==="
                )

                measure_and_save(
                    dataset_name,
                    run,
                    "SelectionSort",
                    original_arr,
                    results_dir,
                    SelectionSort.selection_sort
                )

                measure_and_save(
                    dataset_name,
                    run,
                    "ImprovedSelectionSort",
                    original_arr,
                    results_dir,
                    SelectionSort.improved_selection_sort
                )

                measure_and_save(
                    dataset_name,
                    run,
                    "RecursiveMergeSort",
                    original_arr,
                    results_dir,
                    MergeSort.mergeSort
                )

                measure_and_save(
                    dataset_name,
                    run,
                    "IterativeMergeSort",
                    original_arr,
                    results_dir,
                    MergeSort.mergeSortWithoutRecursion
                )

                measure_and_save(
                    dataset_name,
                    run,
                    "BubbleSort",
                    original_arr,
                    results_dir,
                    BubbleSort.sort
                )

                measure_and_save(
                    dataset_name,
                    run,
                    "BasicBubbleSort",
                    original_arr,
                    results_dir,
                    BubbleSort.sort_basic
                )

                measure_and_save(
                    dataset_name,
                    run,
                    "HeapSort",
                    original_arr,
                    results_dir,
                    HeapSort.sort
                )

                measure_and_save(
                    dataset_name,
                    run,
                    "RecursiveHeapSort",
                    original_arr,
                    results_dir,
                    HeapSort.sort_recursive
                )

                print(
                    "--------------------------------------------"
                )

                array_counter += 1

        except OSError:

            print(
                "Error: The file '"
                + file_path
                + "' does not exist!"
            )

            print(
                "Please check the data directory."
            )


def process_big_data_file(
        file_path,
        results_dir,
        number_of_runs):

    dataset_name = os.path.basename(file_path)

    dataset_name = os.path.splitext(
        dataset_name
    )[0]

    original_arr = read_big_data_file(
        file_path
    )

    print()
    print(
        "Dataset: " + dataset_name
    )

    print(
        "Array length: "
        + str(len(original_arr))
    )

    for run in range(1, number_of_runs + 1):

        print()
        print(
            "============================================"
        )

        print(
            "Dataset: " + dataset_name
        )

        print(
            "Run: "
            + str(run)
            + "/"
            + str(number_of_runs)
        )

        print(
            "Array length: "
            + str(len(original_arr))
        )

        print(
            "============================================"
        )

        measure_and_save(
            dataset_name,
            run,
            "SelectionSort",
            original_arr,
            results_dir,
            SelectionSort.selection_sort
        )

        measure_and_save(
            dataset_name,
            run,
            "ImprovedSelectionSort",
            original_arr,
            results_dir,
            SelectionSort.improved_selection_sort
        )

        measure_and_save(
            dataset_name,
            run,
            "RecursiveMergeSort",
            original_arr,
            results_dir,
            MergeSort.mergeSort
        )

        measure_and_save(
            dataset_name,
            run,
            "IterativeMergeSort",
            original_arr,
            results_dir,
            MergeSort.mergeSortWithoutRecursion
        )

        measure_and_save(
            dataset_name,
            run,
            "BubbleSort",
            original_arr,
            results_dir,
            BubbleSort.sort
        )

        measure_and_save(
            dataset_name,
            run,
            "BasicBubbleSort",
            original_arr,
            results_dir,
            BubbleSort.sort_basic
        )

        measure_and_save(
            dataset_name,
            run,
            "HeapSort",
            original_arr,
            results_dir,
            HeapSort.sort
        )

        measure_and_save(
            dataset_name,
            run,
            "RecursiveHeapSort",
            original_arr,
            results_dir,
            HeapSort.sort_recursive
        )

        print(
            "--------------------------------------------"
        )


def read_arrays_from_file(file_path):

    arrays = []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            tokens = line.replace(
                ",",
                " "
            ).split()

            arr = []

            valid_line = True

            for token in tokens:

                try:

                    arr.append(
                        int(token.strip())
                    )

                except ValueError:

                    valid_line = False

                    print(
                        "Preskacem nevalidan red: "
                        + line
                    )

                    break

            if valid_line and len(arr) > 0:

                arrays.append(arr)

    return arrays


def read_big_data_file(file_path):

    numbers = []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            tokens = line.replace(
                ",",
                " "
            ).split()

            for token in tokens:

                if token:

                    numbers.append(
                        int(token.strip())
                    )

    return numbers


def measure_and_save(
        dataset_name,
        run,
        algo_name,
        original_arr,
        results_dir,
        algorithm):

    if SELECTED_ALGOS is not None and algo_name not in SELECTED_ALGOS:
        return

    arr_copy = original_arr.copy()

    process = psutil.Process(
        os.getpid()
    )

    time.sleep(0.01)

    memory_before = (
        process.memory_info().rss
    )

    start_wall_time = (
        time.perf_counter()
    )

    start_cpu_time = (
        time.process_time()
    )

    sorted_arr = algorithm(
        arr_copy
    )

    end_cpu_time = (
        time.process_time()
    )

    end_wall_time = (
        time.perf_counter()
    )

    memory_after = (
        process.memory_info().rss
    )

    if sorted_arr is None:

        sorted_arr = arr_copy

    wall_time_ms = (
        end_wall_time
        - start_wall_time
    ) * 1000.0

    cpu_time_ms = (
        end_cpu_time
        - start_cpu_time
    ) * 1000.0

    memory_used_kb = max(
        0,
        (
            memory_after
            - memory_before
        ) / 1024.0
    )

    print(
        "  ["
        + algo_name
        + "] (first 10): ",
        end=""
    )

    print_first_ten(
        sorted_arr
    )

    print(
        "    -> Time: "
        + format(
            wall_time_ms,
            ".2f"
        )
        + " ms"
        + " | CPU Time: "
        + format(
            cpu_time_ms,
            ".2f"
        )
        + " ms"
        + " | Memory: "
        + format(
            memory_used_kb,
            ".2f"
        )
        + " KB"
    )

    result_file = os.path.join(
        results_dir,
        algo_name + "Result.csv"
    )

    try:

        with open(
            result_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                dataset_name,
                run,
                len(original_arr),
                format(
                    wall_time_ms,
                    ".2f"
                ),
                format(
                    cpu_time_ms,
                    ".2f"
                ),
                format(
                    memory_used_kb,
                    ".2f"
                )
            ])

    except OSError as e:

        print(
            "Greska pri upisu rezultata za "
            + algo_name
            + ": "
            + str(e)
        )


def print_first_ten(arr):

    limit = min(
        10,
        len(arr)
    )

    first_ten = arr[:limit]

    print(first_ten)


if __name__ == "__main__":
    main()
