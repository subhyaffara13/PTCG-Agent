
def decide_use_async_batching(cb_config: ContinuousBatchingConfig, is_attn_mask_needed: bool) -> None:
    """Returns whether or not to use asynchronous batching for continuous batching. If the user specified this in
    the config, we follow their choice. Otherwise, we turn on asynchronous batching if and only if CUDA graphs are
    turned on and no attention mask is needed.

    This function modifies the `use_async_batching` attribute of the config in place.
    """
    # If the user specifies to use async or not, no need to decide ourselves
    if cb_config.use_async_batching is None:
        use_cuda_graphs = any(cb_config.cuda_graph_booleans)
        cb_config.use_async_batching = use_cuda_graphs and not is_attn_mask_needed
        logger.info(
            f"No behavior specified for use_async_batching, choosing {cb_config.use_async_batching = } because "
            f"{use_cuda_graphs = } and {is_attn_mask_needed = }. If you want to save memory, you can "
            "disable asynchronous batching but it will degrade performance."
        )

