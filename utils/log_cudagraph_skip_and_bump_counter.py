
def log_cudagraph_skip_and_bump_counter(msg: str) -> None:
    cudagraphs_log.warning(msg)
    counters["inductor"]["cudagraph_skips"] += 1

    if torch._inductor.config.triton.cudagraph_or_error:
        raise RuntimeError(msg)

    metrics_context = get_metrics_context()
    if metrics_context.in_progress():
        metrics_context.set("cudagraph_skip_reason", msg, overwrite=True)

