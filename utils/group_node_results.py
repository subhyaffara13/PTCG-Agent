
def group_node_results(sess_time):
    """Group results by operator name.

    Args:
        sess_time (List[Dict]): profile data

    Returns:
        List[str]: lines of string for output.
    """
    op_kernel_time = {}
    op_kernel_records = {}
    total_kernel_time = 0

    provider_op_kernel_time = {}
    provider_op_kernel_records = {}
    provider_kernel_time = {}

    op_fence_time = {}
    total_fence_time = 0

    provider_counter = {}
    for item in sess_time:
        if item["cat"] == "Node" and "dur" in item and "args" in item and "op_name" in item["args"]:
            op_name = item["args"]["op_name"]

            # TODO: shall we have a separated group for nodes with subgraph?
            if op_name in _NODES_TYPE_CONTAINING_SUBGRAPH:
                continue

            if "provider" not in item["args"]:
                if "fence" in item["name"]:
                    if op_name in op_fence_time:
                        op_fence_time[op_name] += item["dur"]
                    else:
                        op_fence_time[op_name] = item["dur"]
                    total_fence_time += item["dur"]
                continue

            provider = item["args"].get("provider", "")
            if provider in provider_counter:
                provider_counter[provider] += 1
            else:
                provider_counter[provider] = 1

            key = f"{provider}:{op_name}"
            if key in provider_op_kernel_time:
                provider_op_kernel_time[key] += item["dur"]
                provider_op_kernel_records[key] += 1
            else:
                provider_op_kernel_time[key] = item["dur"]
                provider_op_kernel_records[key] = 1

            if provider in provider_kernel_time:
                provider_kernel_time[provider] += item["dur"]
            else:
                provider_kernel_time[provider] = item["dur"]

            if op_name in op_kernel_time:
                op_kernel_time[op_name] += item["dur"]
                op_kernel_records[op_name] += 1
            else:
                op_kernel_time[op_name] = item["dur"]
                op_kernel_records[op_name] = 1

            total_kernel_time += item["dur"]

    lines = ["", "Grouped by operator"]
    lines.append("-" * 64)
    lines.append("Total(μs)\tTime%\tKernel(μs)\tKernel%\tCalls\tAvgKernel(μs)\tFence(μs)\tOperator")
    for op_name, kernel_time in sorted(op_kernel_time.items(), key=lambda x: x[1], reverse=True):
        fence_time = op_fence_time.get(op_name, 0)
        kernel_time_ratio = kernel_time / total_kernel_time
        total_time = kernel_time + fence_time
        time_ratio = total_time / (total_kernel_time + total_fence_time)
        kernel_calls = op_kernel_records[op_name]
        avg_kernel_time = kernel_time / kernel_calls
        lines.append(
            f"{total_time:10d}\t{time_ratio * 100.0:5.2f}\t{kernel_time:11d}\t{kernel_time_ratio * 100.0:5.2f}\t{kernel_calls:5d}\t{avg_kernel_time:14.1f}\t{fence_time:10d}\t{op_name}"
        )

    lines += ["", "Grouped by provider + operator"]
    lines.append("-" * 64)
    lines.append("Kernel(μs)\tProvider%\tCalls\tAvgKernel(μs)\tProvider\tOperator")
    for key, kernel_time in sorted(provider_op_kernel_time.items(), key=lambda x: x[1], reverse=True):
        parts = key.split(":")
        provider = parts[0]
        op_name = parts[1]
        short_ep = provider.replace("ExecutionProvider", "")
        calls = provider_op_kernel_records[key]
        avg_kernel_time = kernel_time / calls
        provider_time_ratio = kernel_time / provider_kernel_time[provider]
        lines.append(
            f"{kernel_time:10d}\t{provider_time_ratio * 100.0:9.2f}\t{calls:5d}\t{avg_kernel_time:14.1f}\t{short_ep:8s}\t{op_name}"
        )

    return lines

