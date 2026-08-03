from typing import Any

def output_details(results, csv_filename):
    with open(csv_filename, mode="a", newline="", encoding="ascii") as csv_file:
        column_names = [
            "engine",
            "version",
            "providers",
            "device",
            "precision",
            "optimizer",
            "io_binding",
            "model_name",
            "inputs",
            "threads",
            "batch_size",
            "sequence_length",
            "custom_layer_num",
            "datetime",
            "test_times",
            "QPS",
            "average_latency_ms",
            "latency_variance",
            "latency_90_percentile",
            "latency_95_percentile",
            "latency_99_percentile",
        ]

        csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
        csv_writer.writeheader()
        for result in results:
            csv_writer.writerow(result)

    logger.info(f"Detail results are saved to csv file: {csv_filename}")


def output_details(results: list[dict[str, Any]], csv_filename: str):
    """Output a CSV file with detail of each test results.

    Args:
        results (List[Dict[str, Any]]): list of JSON results.
        csv_filename (str): path of output CSV file
    """
    with open(csv_filename, mode="a", newline="", encoding="ascii") as csv_file:
        column_names = [
            "pretrained_model_name",
            "onnx_path",
            "provider",
            "disable_fused_attention",
            "batch_size",
            "sequence_length",
            "use_io_binding",
            "exact",
            "f1",
            "total",
            "HasAns_exact",
            "HasAns_f1",
            "HasAns_total",
            "best_exact",
            "best_exact_thresh",
            "best_f1",
            "best_f1_thresh",
            "total_time_in_seconds",
            "samples_per_second",
            "latency_in_seconds",
        ]

        csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
        csv_writer.writeheader()
        for result in results:
            csv_writer.writerow(result)

        csv_file.flush()

    print(f"Detail results are saved to csv file: {csv_filename}")


def output_details(results, csv_filename):
    latency_results = [result for result in results if "average_latency_ms" in result]
    if len(latency_results) == 0:
        print("No latency results for output.")
        return

    with open(csv_filename, mode="a", newline="", encoding="ascii") as csv_file:
        column_names = [
            "engine",
            "version",
            "device",
            "precision",
            "optimizer",
            "io_binding",
            "model_name",
            "inputs",
            "threads",
            "datetime",
            "test_times",
            "description",
            "batch_size",
            "sequence_length",
            "global_length",
            "use_compact_memory",
            "use_half4",
            "diff_max",
            "diff_90_percentile",
            "diff_95_percentile",
            "diff_99_percentile",
            "memory",
            "QPS",
            "average_latency_ms",
            "latency_variance",
            "latency_90_percentile",
            "latency_95_percentile",
            "latency_99_percentile",
        ]

        csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
        csv_writer.writeheader()
        for result in latency_results:
            print(result)
            csv_writer.writerow(result)

        csv_file.flush()

    print(f"Detail results are saved to csv file: {csv_filename}")

