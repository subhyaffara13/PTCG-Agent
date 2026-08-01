
def _compile_end() -> None:
    global _cumulative_compile_time, _t0, _triton_kernel_metrics
    if _t0 is not None:
        t1 = time()
        _cumulative_compile_time += t1 - _t0
        _t0 = None
        # print("CUMULATIVE COMPILE TIME", _cumulative_compile_time)
    if _triton_kernel_metrics:
        # Log triton kernel info
        sorted_info = dict(sorted(_triton_kernel_metrics.items()))
        torch._logging.trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "triton_kernel_info",
                "encoding": "json",
            },
            payload_fn=lambda: json.dumps(sorted_info),
        )
        _triton_kernel_metrics = None

