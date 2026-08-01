
def _build_no_accept_preview(ctx: PromptContext, variant: PromptVariant) -> str:
    # Same as baseline, except the can_accept branch drops the
    # "you would receive [...]" line. The model still knows accepting is
    # legal; it has to compute the resulting allocation itself.
    labels = variant.item_labels
    pool_lines = "\n".join(
        f"  {labels[k]}: {int(ctx.pool.get(k, 0))} {_unit_word(int(ctx.pool.get(k, 0)))}"
        for k in _ITEM_KEYS
    )
    my_value_lines = "\n".join(
        f"  {labels[k]}: {int(ctx.my_values.get(k, 0))}" for k in _ITEM_KEYS
    )
    history_str = _format_history_rich(ctx.state, labels)
    accept_help = _accept_help_no_preview() if ctx.can_accept else _accept_help_opening()
    return _BASELINE_TEMPLATE.format(
        pool_lines=pool_lines,
        my_value_lines=my_value_lines,
        max_turns=ctx.max_turns,
        discount_note=_discount_note_baseline(ctx.discount),
        num_offers=ctx.num_offers,
        turns_left=ctx.turns_left,
        history_str=history_str,
        player_label=ctx.player_id + 1,
        accept_help=accept_help,
    )

