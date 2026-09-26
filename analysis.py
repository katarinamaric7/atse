import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ALGORITHMS = [
    "SelectionSort",
    "ImprovedSelectionSort",
    "IterativeMergeSort",
    "RecursiveMergeSort"
]

METRICS = [
    ("Time", "Vreme (ms)"),
    ("CpuTime", "CPU Vreme (ms)"),
    ("Memory", "Memorija (KB)")
]

DATASETS = ["bigdata", "duplicates", "random"]


def find_result_file(results_dir, algorithm):
    known_names = {
        "SelectionSort": "SelectionSortResult.csv",
        "ImprovedSelectionSort": "ImprovedSelectionSortResult.csv",
        "IterativeMergeSort": "IterativeMergeSortResult.csv",
        "RecursiveMergeSort": "RecursiveMergeSortResult.csv"
    }

    filename = known_names.get(algorithm, f"{algorithm}Result.csv")
    path = os.path.join(results_dir, filename)

    if os.path.isfile(path):
        return path

    if os.path.isdir(results_dir):
        wanted = os.path.splitext(filename)[0].lower()

        for current_file in os.listdir(results_dir):
            current_stem = os.path.splitext(current_file)[0].lower()

            if current_stem == wanted:
                return os.path.join(results_dir, current_file)

    return None


def normalize_column_name(name):
    name = str(name).strip().lower()

    name = re.sub(r"[^a-z0-9]+", "", name)

    return name


def find_column(columns, possible_names):
    normalized = {
        normalize_column_name(col): col
        for col in columns
    }

    for possible in possible_names:
        key = normalize_column_name(possible)
        if key in normalized:
            return normalized[key]

    for col in columns:
        normalized_col = normalize_column_name(col)
        for possible in possible_names:
            normalized_possible = normalize_column_name(possible)
            if normalized_possible in normalized_col:
                return col

    return None


def parse_result_file(file_path, language, algorithm_name, limit=100):
    data = []

    if not file_path or not os.path.exists(file_path):
        print(f"Upozorenje: Fajl ne postoji -> {file_path}")
        return data

    try:
        df = pd.read_csv(
            file_path,
            sep=None,
            engine="python"
        )
    except Exception as e:
        print(f"Greska pri citanju fajla {file_path}: {e}")
        return data

    if df.empty:
        print(f"Upozorenje: Fajl je prazan -> {file_path}")
        return data

    length_col = find_column(
        df.columns,
        ["arraylength"]
    )

    time_col = find_column(
        df.columns,
        ["time"]
    )

    cpu_col = find_column(
        df.columns,
        ["cputime"]
    )

    memory_col = find_column(
        df.columns,
        ["memory"]
    )

    missing = []

    if length_col is None:
        missing.append("duzina niza")
    if time_col is None:
        missing.append("vreme")
    if cpu_col is None:
        missing.append("CPU vreme")
    if memory_col is None:
        missing.append("memorija")

    if missing:
        print(
            f"\nUpozorenje: {os.path.basename(file_path)} "
            f"nema potrebne kolone: {', '.join(missing)}"
        )
        print("Pronadjene kolone:", list(df.columns))
        return data

    df = df.head(limit).copy()

    for col in [length_col, time_col, cpu_col, memory_col]:
        df[col] = pd.to_numeric(
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False),
            errors="coerce"
        )

    df = df.dropna(
        subset=[length_col, time_col, cpu_col, memory_col]
    )

    for _, row in df.iterrows():
        memory = float(row[memory_col])
        memory_col_normalized = normalize_column_name(memory_col)

        if "mb" in memory_col_normalized:
            memory *= 1024.0

        data.append({
            "Dataset": None,
            "Language": language,
            "Algorithm": algorithm_name,
            "Length": int(row[length_col]),
            "Time": float(row[time_col]),
            "CpuTime": float(row[cpu_col]),
            "Memory": memory
        })

    return data


def load_all_data(base_dir):
    all_records = []

    for dataset in DATASETS:
        python_dir = os.path.join(
            base_dir, "results", "python", dataset
        )

        java_dir = os.path.join(
            base_dir, "results", "java", dataset
        )

        print("\n==========================================")
        print(f"UCITAVANJE DATASETA: {dataset.upper()}")
        print("==========================================")

        for algorithm in ALGORITHMS:
            for language, results_dir in [
                ("Python", python_dir),
                ("Java", java_dir)
            ]:
                file_path = find_result_file(results_dir, algorithm)

                if file_path is None:
                    print(
                        f"Upozorenje: nije pronadjen rezultat -> "
                        f"{language} / {dataset} / {algorithm}"
                    )
                    continue

                print(f"Ucitavam: {language} | {dataset} | {algorithm}")

                limit_val = 100 if dataset == "random" else 100

                records = parse_result_file(
                    file_path, language, algorithm, limit=limit_val
                )

                for record in records:
                    record["Dataset"] = dataset

                all_records.extend(records)

    df = pd.DataFrame(all_records)

    if not df.empty:
        df = df.sort_values(
            by=["Dataset", "Algorithm", "Language", "Length"]
        )

    return df


def create_chart(
    df_sub,
    group_by_col,
    metric,
    title,
    file_path,
    use_log=False,
    is_fixed_size=False
):

    if df_sub.empty:
        print(f"Preskacem prazan grafikon: {title}")
        return False

    plt.figure(figsize=(8, 4.5))

    metric_labels = {
        "Time": "Vreme (ms)",
        "CpuTime": "CPU Vreme (ms)",
        "Memory": "Memorija (KB)"
    }

    if is_fixed_size:
        groups = list(df_sub.groupby(group_by_col))
        n_groups = len(groups)
        
        sample_stats = groups[0][1].groupby("Length")[metric].mean().reset_index()
        is_single_length = len(sample_stats) == 1
        
        width = 0.15 if is_single_length else 0.25

        for i, (key, group) in enumerate(groups):
            stats = (
                group
                .groupby("Length")[metric]
                .mean()
                .reset_index()
                .sort_values("Length")
            )

            if stats.empty:
                continue

            x = np.arange(len(stats["Length"]))
            offset = (i - n_groups / 2) * width + width / 2

            plt.bar(
                x + offset,
                stats[metric],
                width,
                label=str(key),
                alpha=0.85
            )

        plt.xticks(x, stats["Length"])
        
        if is_single_length:
            plt.xlim(-0.4, 0.4)

        plt.xlabel("Dužina niza (N)")
    else:
        for key, group in df_sub.groupby(group_by_col):
            clean_df = (
                group
                .groupby("Length")[metric]
                .mean()
                .reset_index()
                .sort_values("Length")
            )

            if clean_df.empty:
                continue

            plt.plot(
                clean_df["Length"],
                clean_df[metric],
                label=str(key),
                linewidth=1.5,
                marker="o",
                markersize=3
            )

        plt.xlabel("Dužina niza (N)")

    if use_log:
        plt.yscale("log")

    plt.title(
        title,
        fontsize=11,
        fontweight="bold"
    )

    plt.ylabel(metric_labels.get(metric, metric))
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        file_path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Kreiran grafikon: {file_path}")

    return True



def generate_charts_for_dataset(
    df_dataset,
    analysis_dir,
    dataset
):
    dataset_dir = os.path.join(analysis_dir, dataset)
    os.makedirs(dataset_dir, exist_ok=True)

    generated = []
    is_fixed = dataset in ["bigdata", "duplicates"]

    # JAVA VS PYTHON
    for algorithm in ALGORITHMS:
        df_algorithm = df_dataset[
            df_dataset["Algorithm"] == algorithm
        ]

        for metric, metric_label in METRICS:
            filename = f"chart_JvsP_{algorithm}_{metric}.png"
            path = os.path.join(dataset_dir, filename)

            title = f"{dataset}: {algorithm} - Java vs Python - {metric_label}"

            if create_chart(df_algorithm, "Language", metric, title, path, is_fixed_size=is_fixed):
                generated.append(path)

    # JAVA - SELECTION SORT
    df_java = df_dataset[df_dataset["Language"] == "Java"]
    df_selection_java = df_java[
        df_java["Algorithm"].isin(["SelectionSort", "ImprovedSelectionSort"])
    ]

    for metric, metric_label in METRICS:
        path = os.path.join(dataset_dir, f"chart_Java_Selection_{metric}.png")
        title = f"{dataset}: Java - SelectionSort vs ImprovedSelectionSort - {metric_label}"

        if create_chart(df_selection_java, "Algorithm", metric, title, path, is_fixed_size=is_fixed):
            generated.append(path)

    # JAVA - MERGE SORT
    df_merge_java = df_java[
        df_java["Algorithm"].isin(["IterativeMergeSort", "RecursiveMergeSort"])
    ]

    for metric, metric_label in METRICS:
        path = os.path.join(dataset_dir, f"chart_Java_Merge_{metric}.png")
        title = f"{dataset}: Java - IterativeMergeSort vs RecursiveMergeSort - {metric_label}"

        if create_chart(df_merge_java, "Algorithm", metric, title, path, is_fixed_size=is_fixed):
            generated.append(path)

    # PYTHON - SELECTION SORT
    df_python = df_dataset[df_dataset["Language"] == "Python"]
    df_selection_python = df_python[
        df_python["Algorithm"].isin(["SelectionSort", "ImprovedSelectionSort"])
    ]

    for metric, metric_label in METRICS:
        path = os.path.join(dataset_dir, f"chart_Python_Selection_{metric}.png")
        title = f"{dataset}: Python - SelectionSort vs ImprovedSelectionSort - {metric_label}"

        if create_chart(df_selection_python, "Algorithm", metric, title, path, is_fixed_size=is_fixed):
            generated.append(path)

    # PYTHON - MERGE SORT
    df_merge_python = df_python[
        df_python["Algorithm"].isin(["IterativeMergeSort", "RecursiveMergeSort"])
    ]

    for metric, metric_label in METRICS:
        path = os.path.join(dataset_dir, f"chart_Python_Merge_{metric}.png")
        title = f"{dataset}: Python - IterativeMergeSort vs RecursiveMergeSort - {metric_label}"

        if create_chart(df_merge_python, "Algorithm", metric, title, path, is_fixed_size=is_fixed):
            generated.append(path)

    return generated


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df_data = load_all_data(base_dir)

    if df_data.empty:
        print("\nGRESKA: Nisu pronadjeni podaci u CSV fajlovima!")
        print("\nOcekivana struktura je:")
        print("results/")
        print("├── java/")
        print("│   ├── bigdata/")
        print("│   ├── duplicates/")
        print("│   └── random/")
        print("└── python/")
        print("    ├── bigdata/")
        print("    ├── duplicates/")
        print("    └── random/")
    else:
        analysis_dir = os.path.join(base_dir, "analysis")
        os.makedirs(analysis_dir, exist_ok=True)

        total_charts = 0

        for dataset in DATASETS:
            df_dataset_sub = df_data[df_data["Dataset"] == dataset]

            if df_dataset_sub.empty:
                print(f"\nNema podataka za dataset: {dataset}")
                continue

            charts = generate_charts_for_dataset(
                df_dataset_sub, analysis_dir, dataset
            )

            total_charts += len(charts)

        print("\n==========================================")
        print("GENERISANJE GRAFIKONA JE ZAVRSENO")
        print(f"Ukupno grafikona: {total_charts}")
        print(f"Lokacija: {analysis_dir}")
        print("==========================================")