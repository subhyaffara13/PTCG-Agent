
def get_peak_memory_runtime_baseline(graph: Graph) -> tuple[int, float]:
    """
    Get the baseline peak memory and runtime.
    Baseline here means there is no FSDP or AC.
    Memory includes the parameters, gradients, activations, and activation gradients.
    Memory does not include e.g., optimizer states, embedding tables, etc.

    Returns:
        int: peak memory in bytes
        float: compute time in ms
    """
    P_1 = graph.nodes[0]["param_per_module"]
    num_nodes = len(graph.nodes)
    peak_mem = 0
    for i in range(num_nodes):
        TG_i = graph.nodes[i]["grad_total"]
        AG_i = graph.nodes[i]["act_grad_per_module"]
        TA_i = graph.nodes[i]["act_total"]
        peak_mem = max(peak_mem, P_1 + TG_i + AG_i + TA_i)
    compute_time = (
        graph.nodes[0]["fw_runtime_per_module"]
        + graph.nodes[0]["bw_runtime_per_module"]
    )
    return (peak_mem, compute_time)

