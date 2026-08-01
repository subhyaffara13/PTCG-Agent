
def register_cp_sharding_rules():
    """Register Context Parallelism sharding rules for all scaled_dot_product ops."""
    global _cp_strategy_contexts, _original_strategies

    # If already registered, don't register again
    if _cp_strategy_contexts:
        return

    # Define ops and their corresponding CP strategy functions
    cp_strategies = [
        (
            aten._scaled_dot_product_flash_attention.default,
            _scaled_dot_product_flash_attention_cp_strategy,
            RuntimeSchemaInfo(5),
        ),
        (
            aten._scaled_dot_product_flash_attention_backward.default,
            _scaled_dot_product_flash_attention_backward_cp_strategy,
            None,
        ),
        (
            aten._scaled_dot_product_efficient_attention.default,
            _scaled_dot_product_efficient_attention_cp_strategy,
            RuntimeSchemaInfo(4),
        ),
        (
            aten._scaled_dot_product_efficient_attention_backward.default,
            _scaled_dot_product_efficient_attention_backward_cp_strategy,
            None,
        ),
        (
            aten._scaled_dot_product_cudnn_attention.default,
            _scaled_dot_product_cudnn_attention_cp_strategy,
            RuntimeSchemaInfo(4),
        ),
        (
            aten._scaled_dot_product_cudnn_attention_backward.default,
            _scaled_dot_product_cudnn_attention_backward_cp_strategy,
            None,
        ),
    ]

    # Register each strategy
    for op_overload, strategy_func, schema_info in cp_strategies:
        ctx = _op_strategy_context(op_overload, strategy_func, schema_info)
        orig_funcs, orig_schema = ctx.__enter__()
        _cp_strategy_contexts[op_overload] = ctx
        _original_strategies[op_overload] = (orig_funcs, orig_schema)

