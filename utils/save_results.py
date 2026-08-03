import sys
from pathlib import Path


def save_results(
    results: LinterStats, base: str | Path, pylint_home: str | Path = PYLINT_HOME
) -> None:
    base = Path(base)
    pylint_home = Path(pylint_home)
    try:
        pylint_home.mkdir(parents=True, exist_ok=True)
    except OSError:  # pragma: no cover
        print(f"Unable to create directory {pylint_home}", file=sys.stderr)
    data_file = _get_pdata_path(base, 1)
    try:
        with open(data_file, "wb") as stream:
            pickle.dump(results, stream)
    except OSError as ex:  # pragma: no cover
        print(f"Unable to create file {data_file}: {ex}", file=sys.stderr)


def save_results(results, filename):
    import pandas as pd  # noqa: PLC0415

    df = pd.DataFrame(
        results,
        columns=[
            "Warmup Runs",
            "Measured Runs",
            "Model Name",
            "Engine",
            "Precision",
            "Device",
            "Batch Size",
            "Sequence Length",
            "Step",
            "Latency (s)",
            "Latency (ms)",
            "Throughput (tps)",
            "Memory (GB)",
        ],
    )

    # Set column types
    df["Warmup Runs"] = df["Warmup Runs"].astype("int")
    df["Measured Runs"] = df["Measured Runs"].astype("int")
    df["Batch Size"] = df["Batch Size"].astype("int")
    df["Sequence Length"] = df["Sequence Length"].astype("int")
    df["Latency (s)"] = df["Latency (s)"].astype("float")
    df["Latency (ms)"] = df["Latency (ms)"].astype("float")
    df["Throughput (tps)"] = df["Throughput (tps)"].astype("float")
    df["Memory (GB)"] = df["Memory (GB)"].astype("float")

    # get package name and version
    import pkg_resources  # noqa: PLC0415

    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(
        [f"{i.key}=={i.version}" for i in installed_packages if i.key in ["onnxruntime", "onnxruntime-gpu"]]
    )

    ort_pkg_name = ""
    ort_pkg_version = ""
    if installed_packages_list:
        ort_pkg_name = installed_packages_list[0].split("==")[0]
        ort_pkg_version = installed_packages_list[0].split("==")[1]

    # Save results to csv with standard format
    records = []
    for _, row in df.iterrows():
        if row["Engine"] in ["optimum-ort", "onnxruntime"]:
            record = BenchmarkRecord(
                row["Model Name"], row["Precision"], "onnxruntime", row["Device"], ort_pkg_name, ort_pkg_version
            )
        elif row["Engine"] in ["pytorch-eager", "pytorch-compile"]:
            record = BenchmarkRecord(
                row["Model Name"], row["Precision"], "pytorch", row["Device"], torch.__name__, torch.__version__
            )
        else:
            record = BenchmarkRecord(row["Model Name"], row["Precision"], row["Engine"], row["Device"], "", "")
        record.config.warmup_runs = row["Warmup Runs"]
        record.config.measured_runs = row["Measured Runs"]
        record.config.batch_size = row["Batch Size"]
        record.config.seq_length = row["Sequence Length"]
        record.config.customized["measure_step"] = row["Step"]
        record.config.customized["engine"] = row["Engine"]
        record.metrics.customized["latency_s_mean"] = row["Latency (s)"]
        record.metrics.latency_ms_mean = row["Latency (ms)"]
        record.metrics.customized["throughput_tps"] = row["Throughput (tps)"]
        record.metrics.max_memory_usage_GB = row["Memory (GB)"]

        records.append(record)

    BenchmarkRecord.save_as_csv(filename, records)
    BenchmarkRecord.save_as_json(filename.replace(".csv", ".json"), records)
    logger.info(f"Results saved in {filename}!")


def save_results(results, filename, gen_length):
    df = pd.DataFrame(
        results,
        columns=[
            "Batch Size",
            "Prompt Length",
            "Prompt Processing Latency (ms)",
            "Prompt Processing Throughput (tps)",
            "Sampling Latency (ms)",
            "Sampling Throughput (tps)",
            "First Token Generated Latency (ms)",
            "First Token Generated Throughput (tps)",
            f"Average Latency of First {gen_length // 2} Tokens Generated (ms)",
            f"Average Throughput of First {gen_length // 2} Tokens Generated (tps)",
            f"Average Latency of First {gen_length} Tokens Generated (ms)",
            f"Average Throughput of First {gen_length} Tokens Generated (tps)",
            "Wall-Clock Latency (s)",
            "Wall-Clock Throughput (tps)",
        ],
    )

    df.to_csv(filename, index=False)
    logger.info(f"Results saved in {filename}!")


def save_results(results, filename):
    import pandas as pd  # noqa: PLC0415

    df = pd.DataFrame(
        results,
        columns=[
            "Warmup Runs",
            "Measured Runs",
            "Model Name",
            "Engine",
            "Precision",
            "Device",
            "Audio File",
            "Duration (s)",
            "Token Length",
            "Load Audio Latency (s)",
            "Load Audio Throughput (qps)",
            "Feature Extractor Latency (s)",
            "Feature Extractor Throughput (qps)",
            "Latency (s)",
            "Per Token Latency (ms/token)",
            "Throughput (qps)",
            "Memory (GB)",
            "Real Time Factor (RTF)",
        ],
    )

    # Set column types
    df["Warmup Runs"] = df["Warmup Runs"].astype("int")
    df["Measured Runs"] = df["Measured Runs"].astype("int")
    df["Duration (s)"] = df["Duration (s)"].astype("float")
    df["Token Length"] = df["Token Length"].astype("int")
    df["Load Audio Latency (s)"] = df["Load Audio Latency (s)"].astype("float")
    df["Load Audio Throughput (qps)"] = df["Load Audio Throughput (qps)"].astype("float")
    df["Feature Extractor Latency (s)"] = df["Feature Extractor Latency (s)"].astype("float")
    df["Feature Extractor Throughput (qps)"] = df["Feature Extractor Throughput (qps)"].astype("float")
    df["Latency (s)"] = df["Latency (s)"].astype("float")
    df["Per Token Latency (ms/token)"] = df["Per Token Latency (ms/token)"].astype("float")
    df["Throughput (qps)"] = df["Throughput (qps)"].astype("float")
    df["Memory (GB)"] = df["Memory (GB)"].astype("float")
    df["Real Time Factor (RTF)"] = df["Real Time Factor (RTF)"].astype("float")

    # get package name and version
    import pkg_resources  # noqa: PLC0415

    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(
        [f"{i.key}=={i.version}" for i in installed_packages if i.key in ["onnxruntime", "onnxruntime-gpu"]]
    )
    ort_pkg_name = ""
    ort_pkg_version = ""
    if installed_packages_list:
        ort_pkg_name = installed_packages_list[0].split("==")[0]
        ort_pkg_version = installed_packages_list[0].split("==")[1]

    # Save results to csv with standard format
    records = []
    for _, row in df.iterrows():
        if row["Engine"] == "onnxruntime":
            record = BenchmarkRecord(
                row["Model Name"], row["Precision"], row["Engine"], row["Device"], ort_pkg_name, ort_pkg_version
            )
        else:
            record = BenchmarkRecord(
                row["Model Name"], row["Precision"], row["Engine"], row["Device"], torch.__name__, torch.__version__
            )
        record.config.customized["audio_file"] = row["Audio File"]
        record.config.warmup_runs = row["Warmup Runs"]
        record.config.measured_runs = row["Measured Runs"]

        record.metrics.customized["duration"] = row["Duration (s)"]
        record.metrics.customized["token_length"] = row["Token Length"]
        record.metrics.customized["load_audio_latency"] = row["Load Audio Latency (s)"]
        record.metrics.customized["load_audio_throughput"] = row["Load Audio Throughput (qps)"]
        record.metrics.customized["feature_extractor_latency_s"] = row["Feature Extractor Latency (s)"]
        record.metrics.customized["feature_extractor_throughput_qps"] = row["Feature Extractor Throughput (qps)"]
        record.metrics.customized["per_token_latency_ms"] = row["Per Token Latency (ms/token)"]
        record.metrics.customized["rtf"] = row["Real Time Factor (RTF)"]

        record.metrics.latency_ms_mean = row["Latency (s)"] * 1000
        record.metrics.throughput_qps = row["Throughput (qps)"]
        record.metrics.max_memory_usage_GB = row["Memory (GB)"]

        records.append(record)

    BenchmarkRecord.save_as_csv(filename, records)
    BenchmarkRecord.save_as_json(filename.replace(".csv", ".json"), records)
    logger.info(f"Results saved in {filename}!")

