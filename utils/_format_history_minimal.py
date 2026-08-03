from typing import Any

def _format_history_minimal(state: Mapping[str, Any], labels: Mapping[str, str]) -> str:
    """Terser history: just ``Px keep: L1=A L2=B L3=C`` per row, no complement."""
    history = state.get("offer_history") or []
    if not history:
        return "  (none)"
    lines: list[str] = []
    for event in history:
        player = int(event.get("player", 0))
        who = f"P{player + 1}"
        if event.get("type") == "agree":
            lines.append(f"  {who} agree")
            continue
        items = event.get("items") or {}
        parts = " ".join(f"{labels[k]}={int(items.get(k, 0))}" for k in _ITEM_KEYS)
        lines.append(f"  {who} keep: {parts}")
    return "\n".join(lines)

