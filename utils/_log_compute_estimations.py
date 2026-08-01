
def _log_compute_estimations(
    compute_nodes: list[fx.Node],
    benchmarked_estimations: list[float],
    analytical_estimations: list[float],
) -> None:
    """Log compute node runtime estimations comparing benchmarked vs analytical."""
    import torch.utils._pytree as pytree
    from torch._inductor.fx_utils import count_flops_fx
    from torch.utils._dtype_abbrs import dtype_abbrs

    def _node_summary(n: fx.Node) -> str:
        ret = str(n)
        for arg in pytree.arg_tree_leaves(n.args, n.kwargs):
            if not isinstance(arg, torch.fx.Node):
                continue
            if "val" in arg.meta:
                t = arg.meta["val"]
                ret += f" {dtype_abbrs[t.dtype]}{tuple(t.shape)}"
        return ret

    headers = [
        "Node",
        "Benchmarked Est(us)",
        "Analytical Est(us)",
        "Diff(ratio)",
        "Diff(us)",
        "Flops",
    ]

    rows = [
        [
            _node_summary(node),
            f"{est_b * 1e3:.4f}",
            f"{est_a * 1e3:.4f}",
            f"{(est_a / est_b) if est_b > 0 else 0:.4f}",
            f"{(est_a - est_b) * 1e3:.4f}",
            str(count_flops_fx(node)),
        ]
        for node, est_b, est_a in zip(
            compute_nodes, benchmarked_estimations, analytical_estimations
        )
    ]

    log_str = _format_csv(headers, rows)

    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "fx_compute_nodes_runtime_estimation",
            "encoding": "string",
        },
        payload_fn=lambda: log_str,
    )

