
def resolve_using_hints(cb_config: ContinuousBatchingConfig, workload_hints: WorkloadHints | None) -> None:
    """Fills some attributes from the workload hints, when the user did not set it explicitly: `max_blocks_per_request`
    and `max_requests_per_batch`."""
    # The max number of blocks per request is an even number large enough to hold the max request length
    if cb_config.max_blocks_per_request is None and workload_hints is not None:
        max_sequence_length = workload_hints.max_prompt_length + workload_hints.max_generated_length
        if max_sequence_length > 0:
            blocks_per_request = int(ceil(max_sequence_length / cb_config.block_size)) + 1
            cb_config.max_blocks_per_request = blocks_per_request + (blocks_per_request % 2)
    # The maximum number of requests per batch is the minimum of the workload hints and the fallback default
    if cb_config.max_requests_per_batch is None and workload_hints is not None:
        if workload_hints.num_requests > 0:  # guard against bad hints
            max_requests_per_batch = min(workload_hints.num_requests, FALLBACK_DEFAULTS["max_requests_per_batch"])
        else:
            max_requests_per_batch = FALLBACK_DEFAULTS["max_requests_per_batch"]
        cb_config.max_requests_per_batch = max_requests_per_batch

