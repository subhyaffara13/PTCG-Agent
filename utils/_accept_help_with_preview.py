
def _accept_help_with_preview(ctx: PromptContext, labels: Mapping[str, str]) -> str:
    accepted_items = (ctx.last_offer_event or {}).get("items") or {}
    you_would_receive = _complement(accepted_items, ctx.pool)
    return (
        "You MAY accept the opponent's most recent offer with"
        ' `{"action": "agree"}`. If you accept, you would receive '
        f"[{_format_items_dict(you_would_receive, labels)}] (their offer to you)."
    )

