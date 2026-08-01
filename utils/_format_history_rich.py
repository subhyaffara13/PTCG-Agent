
def _format_history_rich(state: Mapping[str, Any], labels: Mapping[str, str]) -> str:
    """Numbered timeline showing both ``keep`` and the complement per offer."""
    history = state.get("offer_history") or []
    pool = state.get("pool") or {}
    if not history:
        return "(no offers yet -- you are opening the negotiation)"
    lines: list[str] = []
    for i, event in enumerate(history, start=1):
        player = int(event.get("player", 0))
        who = f"Player {player + 1}"
        if event.get("type") == "agree":
            lines.append(f"  {i}. {who} ACCEPTS the previous offer (game ends).")
            continue
        items = event.get("items") or {}
        offered = _complement(items, pool)
        lines.append(
            f"  {i}. {who} offers: keep [{_format_items_dict(items, labels)}]"
            f" / opponent gets [{_format_items_dict(offered, labels)}]"
        )
    return "\n".join(lines)

