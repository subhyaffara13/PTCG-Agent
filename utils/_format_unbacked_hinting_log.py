
def _format_unbacked_hinting_log(
    op_schema: OpSchema,
    strategies: list[OpSpec],
    strategy_index: int,
    replacements: dict,
) -> str:
    """Format log message for unbacked hinting strategy selection (only called if debug logging enabled)."""
    args_spec = tuple(str(spec) for spec in op_schema.args_schema)
    strat = strategies[strategy_index]
    if strat.input_specs is None:
        placements_in = None
    else:
        placements_in = tuple(
            spec.format_shard_order_str(spec.placements, spec.shard_order)
            for spec in strat.input_specs
        )
    placements_out = tree_map(
        lambda spec: spec.format_shard_order_str(spec.placements, spec.shard_order),
        strat.output_specs,
        is_leaf=lambda x: isinstance(x, DTensorSpec),
    )
    return (
        f"Selected strategy {placements_in} -> {placements_out} "
        f"for {op_schema.op} with input {args_spec}, using unbacked hints: {replacements}"
    )

