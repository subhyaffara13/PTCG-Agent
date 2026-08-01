
def _build_compact(ctx: PromptContext, variant: PromptVariant) -> str:
    labels = variant.item_labels
    pool_inline = ", ".join(f"{labels[k]} {int(ctx.pool.get(k, 0))}" for k in _ITEM_KEYS)
    values_inline = ", ".join(
        f"{labels[k]} {int(ctx.my_values.get(k, 0))}" for k in _ITEM_KEYS
    )
    history_str = _format_history_rich(ctx.state, labels)
    accept_help = (
        _accept_help_with_preview(ctx, labels) if ctx.can_accept else _accept_help_opening()
    )
    return _COMPACT_TEMPLATE.format(
        player_label=ctx.player_id + 1,
        pool_inline=pool_inline,
        values_inline=values_inline,
        max_turns=ctx.max_turns,
        discount_note=_discount_note_baseline(ctx.discount),
        num_offers=ctx.num_offers,
        history_str=history_str,
        accept_help=accept_help,
    )

