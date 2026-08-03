from typing import Any

def output_summary(results, csv_filename, args):
    with open(csv_filename, mode="a", newline="", encoding="ascii") as csv_file:
        header_names = [
            "model_name",
            "inputs",
            "custom_layer_num",
            "engine",
            "version",
            "providers",
            "device",
            "precision",
            "optimizer",
            "io_binding",
            "threads",
        ]
        data_names = []
        for batch_size in args.batch_sizes:
            if args.sequence_lengths == [""]:
                data_names.append(f"b{batch_size}")
            else:
                for sequence_length in args.sequence_lengths:
                    data_names.append(f"b{batch_size}_s{sequence_length}")

        csv_writer = csv.DictWriter(csv_file, fieldnames=header_names + data_names)
        csv_writer.writeheader()
        for model_name in args.models:
            for input_count in [1, 2, 3]:
                for engine_name in args.engines:
                    for io_binding in [True, False, ""]:
                        for threads in args.num_threads:
                            row = {}
                            for result in results:
                                if (
                                    result["model_name"] == model_name
                                    and result["inputs"] == input_count
                                    and result["engine"] == engine_name
                                    and result["io_binding"] == io_binding
                                    and result["threads"] == threads
                                ):
                                    headers = {k: v for k, v in result.items() if k in header_names}
                                    if not row:
                                        row.update(headers)
                                        row.update(dict.fromkeys(data_names, ""))
                                    else:
                                        for k in header_names:
                                            assert row[k] == headers[k]
                                    b = result["batch_size"]
                                    s = result["sequence_length"]
                                    if s:
                                        row[f"b{b}_s{s}"] = result["average_latency_ms"]
                                    else:
                                        row[f"b{b}"] = result["average_latency_ms"]
                            if row:
                                csv_writer.writerow(row)

    logger.info(f"Summary results are saved to csv file: {csv_filename}")


def output_summary(results: list[dict[str, Any]], csv_filename: str, metric_name: str):
    """Output a CSV file with summary of a metric on combinations of batch_size and sequence_length.

    Args:
        results (List[Dict[str, Any]]): list of JSON results.
        csv_filename (str): path of output CSV file
        metric_name (str): the metric to summarize
    """
    with open(csv_filename, mode="a", newline="", encoding="ascii") as csv_file:
        header_names = [
            "pretrained_model_name",
            "onnx_path",
            "provider",
            "disable_fused_attention",
            "use_io_binding",
        ]

        model_list = list({result["onnx_path"] for result in results})
        model_list.sort()

        batch_sizes = list({result["batch_size"] for result in results})
        batch_sizes.sort()

        sequence_lengths = list({result["sequence_length"] for result in results})
        sequence_lengths.sort()

        key_names = []
        for sequence_length in sequence_lengths:
            for batch_size in batch_sizes:
                key_names.append(f"b{batch_size}_s{sequence_length}")

        csv_writer = csv.DictWriter(csv_file, fieldnames=header_names + key_names)
        csv_writer.writeheader()

        for model in model_list:
            row = {}

            # Metric value for given pair of batch_size and sequence_length.
            # Assume that (onnx_path, batch_size and sequence_length) are unique so keep first occurrence only.
            values = {}
            values.update(dict.fromkeys(key_names, ""))

            for result in results:
                if result["onnx_path"] == model and result[metric_name]:
                    headers = {k: v for k, v in result.items() if k in header_names}
                    if not row:
                        row.update(headers)

                    batch_size = result["batch_size"]
                    sequence_length = result["sequence_length"]
                    key = f"b{batch_size}_s{sequence_length}"

                    if key in key_names:
                        values[key] = result[metric_name]

            if row:
                for key in key_names:
                    row[key] = values.get(key, "")
                csv_writer.writerow(row)

        csv_file.flush()

    print(f"Summary results for {metric_name} are saved to csv file: {csv_filename}")


def output_summary(results, csv_filename, data_field="average_latency_ms"):
    with open(csv_filename, mode="a", newline="", encoding="ascii") as csv_file:
        header_names = [
            "model_name",
            "precision",
            "engine",
            "version",
            "global_length",
            "use_compact_memory",
            "use_half4",
            "description",
        ]

        description_list = list({result["description"] for result in results})
        description_list.sort()

        batch_sizes = list({result["batch_size"] for result in results})
        batch_sizes.sort()

        sequence_lengths = list({result["sequence_length"] for result in results})
        sequence_lengths.sort()

        data_names = []
        for sequence_length in sequence_lengths:
            for batch_size in batch_sizes:
                data_names.append(f"b{batch_size}_s{sequence_length}")

        csv_writer = csv.DictWriter(csv_file, fieldnames=header_names + data_names)
        csv_writer.writeheader()

        for description in description_list:
            row = {}

            sum_latency = {}
            sum_latency.update(dict.fromkeys(data_names, 0))

            count_latency = {}
            count_latency.update(dict.fromkeys(data_names, 0))

            for result in results:
                if result["description"] == description and result[data_field]:
                    headers = {k: v for k, v in result.items() if k in header_names}
                    if not row:
                        row.update(headers)
                    else:
                        for k in header_names:
                            if row[k] != headers[k]:
                                raise RuntimeError("Description shall be unique")

                    batch_size = result["batch_size"]
                    sequence_length = result["sequence_length"]
                    key = f"b{batch_size}_s{sequence_length}"

                    try:
                        latency = float(result[data_field])
                    except ValueError:
                        continue

                    sum_latency[key] += latency
                    count_latency[key] += 1

            if row:
                for key in data_names:
                    if key in count_latency and count_latency[key] > 0:
                        row[key] = sum_latency[key] / count_latency[key]
                    else:
                        row[key] = ""

                csv_writer.writerow(row)

        csv_file.flush()

