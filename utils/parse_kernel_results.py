
def parse_kernel_results(sess_time, threshold=0):
    """Parse profile data and output nodes in two sections - nodes in the original order, and top expensive nodes.

    Args:
        sess_time (List[Dict]): profile data
        threshold (int, optional): Minimum ratio of duration among all. Defaults to 0.

    Returns:
        List[str]: lines of string for output.
    """
    kernel_name_to_op_name = {}
    kernel_time = {}
    kernel_freq = {}
    total = 0
    session_init = False
    for item in sess_time:
        # Skip all MemcpyHostToDevice before session_initialization
        if item["cat"] == "Session" and item["name"] == "session_initialization":
            session_init = True
        if not session_init:
            continue

        if item["cat"] == "Kernel" and "dur" in item and "args" in item and "op_name" in item["args"]:
            kernel_name = item["name"]

            op_name = item["args"]["op_name"]
            if op_name in _NODES_TYPE_CONTAINING_SUBGRAPH:
                continue

            # Handle MemcpyHostToDevice and MemcpyDeviceToHost here
            if not op_name:
                op_name = f"({kernel_name})"

            if kernel_name in kernel_time:
                kernel_time[kernel_name] += item["dur"]
                kernel_freq[kernel_name] += 1
            else:
                kernel_time[kernel_name] = item["dur"]
                kernel_freq[kernel_name] = 1
                kernel_name_to_op_name[kernel_name] = op_name

            total += item["dur"]

    if not kernel_time:
        return ["No kernel record found!"]

    # Output items with run time ratio > thresholds, and sorted by duration in the descending order.
    lines = []
    lines.append(f"\nTop expensive kernels with Time% >= {threshold * 100:.2f}:")
    lines.append("-" * 64)
    lines.append("Total(μs)\tTime%\tCalls\tAvg(μs)\tKernel")
    for kernel_name, duration in sorted(kernel_time.items(), key=lambda x: x[1], reverse=True):
        ratio = duration / total
        if ratio < threshold:
            continue

        calls = kernel_freq[kernel_name]
        avg_time = duration / float(calls)
        lines.append(f"{duration:10d}\t{ratio * 100.0:5.2f}\t{calls:5d}\t{avg_time:8.1f}\t{kernel_name}")

    # Group by operator
    op_time = {}
    for kernel_name, op_name in kernel_name_to_op_name.items():
        duration = kernel_time[kernel_name]
        if op_name in op_time:
            op_time[op_name] += duration
        else:
            op_time[op_name] = duration

    lines.append("\nGroup kernel time by operator:")
    lines.append("-" * 64)
    lines.append("Total(μs)\tTime%\tOperator")
    for op_name, duration in sorted(op_time.items(), key=lambda x: x[1], reverse=True):
        ratio = duration / total
        lines.append(f"{duration:10d}\t{ratio * 100.0:5.2f}\t{op_name}")

    return lines

