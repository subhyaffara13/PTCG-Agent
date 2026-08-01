
def _build_minimal_with_goal(ctx: PromptContext, variant: PromptVariant) -> str:
    labels = variant.item_labels
    pool_inline = " ".join(f"{labels[k]}={int(ctx.pool.get(k, 0))}" for k in _ITEM_KEYS)
    values_inline = " ".join(
        f"{labels[k]}={int(ctx.my_values.get(k, 0))}" for k in _ITEM_KEYS
    )
    history_str = _format_history_minimal(ctx.state, labels)
    return _MINIMAL_WITH_GOAL_TEMPLATE.format(
        player_label=ctx.player_id + 1,
        pool_inline=pool_inline,
        values_inline=values_inline,
        max_turns=ctx.max_turns,
        history_str=history_str,
    )

