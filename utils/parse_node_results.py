
def parse_node_results(sess_time, kernel_time_only=False, threshold=0):
    """Parse profile data and output nodes in two sections - nodes in the original order, and top expensive nodes.

    Args:
        sess_time (List[Dict]): profile data
        kernel_time_only (bool, optional): Only include items for kernel time. Defaults to False.
        threshold (int, optional): Minimum ratio of duration among all. Defaults to 0.

    Returns:
        List[str]: lines of string for output.
    """
    node_name_list = []
    node_time = {}
    node_freq = {}
    node_provider = {}
    total = 0
    for item in sess_time:
        if item["cat"] == "Node" and "dur" in item and "args" in item and "op_name" in item["args"]:
            node_name = (
                item["name"].replace("_kernel_time", "").replace("_fence_before", "").replace("_fence_after", "")
            )

            if "provider" in item["args"]:
                if item["args"]["provider"] == "CPUExecutionProvider":
                    device = "CPU"
                elif item["args"]["provider"] == "CUDAExecutionProvider":
                    device = "CUDA"
                elif item["args"]["provider"] == "DmlExecutionProvider":
                    device = "DML"

                if node_name not in node_provider:
                    node_provider[node_name] = device
                else:
                    assert node_provider[node_name] == device
            elif kernel_time_only:
                continue

            op_name = item["args"]["op_name"]
            if op_name in _NODES_TYPE_CONTAINING_SUBGRAPH:
                continue

            if node_name in node_time:
                node_time[node_name] += item["dur"]
                node_freq[node_name] += 1
            else:
                node_time[node_name] = item["dur"]
                node_freq[node_name] = 1
                node_name_list.append(node_name)

            total += item["dur"]

    # Output items in the original order.
    lines = [
        "\nNodes in the original order:",
        "-" * 64,
        "Total(μs)\tTime%\tAcc %\tAvg(μs)\tCalls\tProvider\tNode",
    ]
    before_percentage = 0.0
    for node_name in node_name_list:
        duration = node_time[node_name]
        calls = node_freq[node_name]
        avg_time = duration / float(calls)
        percentage = (duration / total) * 100.0
        provider = node_provider.get(node_name, "")
        before_percentage += percentage
        lines.append(
            f"{duration:10d}\t{percentage:5.2f}\t{before_percentage:5.2f}\t{avg_time:8.1f}\t{calls:5d}\t{provider:8s}\t{node_name}"
        )

    # Output items with run time ratio > thresholds, and sorted by duration in the descending order.
    lines.append(f"\nTop expensive nodes with Time% >= {threshold * 100:.2f}:")
    lines.append("-" * 64)
    lines.append("Total(μs)\tTime%\tAvg(μs)\tCalls\tProvider\tNode")
    for node_name, duration in sorted(node_time.items(), key=lambda x: x[1], reverse=True):
        ratio = duration / total
        if ratio < threshold:
            continue

        calls = node_freq[node_name]
        avg_time = duration / float(calls)
        percentage = (duration / total) * 100.0
        provider = node_provider.get(node_name, "")
        lines.append(f"{duration:10d}\t{percentage:5.2f}\t{avg_time:8.1f}\t{calls:5d}\t{provider:8s}\t{node_name}")

    return lines

