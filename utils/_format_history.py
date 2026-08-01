
def _format_history(move_history: list[str]) -> str:
    """Group the flat action list into 3-action turns labelled by player.

    The framework stores ``move_history`` as a flat list of algebraic cells,
    one per sub-action. Without grouping the model sees ``a7, d7, e7, c6,
    c5, c4`` and has to remember "every three cells is one turn, players
    alternate, X started" -- which is undocumented and easy to get wrong.
    Render each completed turn as ``X: a7 -> d7, barrier e7`` instead. Skip
    any partial trailing turn (its squares are surfaced by the prompt's
    source-square disclosure instead, so showing it here would duplicate).
    """
    if len(move_history) < 3:
        return "(no completed turns yet)"
    full_turns = len(move_history) // 3
    start = max(0, full_turns - _HISTORY_MAX_TURNS)
    lines = []
    for t in range(start, full_turns):
        i = t * 3
        from_sq, to_sq, barrier_sq = move_history[i:i + 3]
        player = "X" if t % 2 == 0 else "O"
        lines.append(f"{player}: {from_sq} -> {to_sq}, barrier {barrier_sq}")
    return "\n".join(lines)


def _format_history(state: Mapping[str, Any]) -> str:
    """Render the offer/agree timeline as a numbered list."""
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
            f"  {i}. {who} offers: keep [{_format_items_dict(items)}] / opponent gets [{_format_items_dict(offered)}]"
        )
    return "\n".join(lines)


def _format_history(move_history: list[str]) -> str:
    if not move_history:
        return "(no moves yet)"
    return ", ".join(move_history)


def _format_history(state: Mapping[str, Any]) -> str:
    proposals = state.get("proposals") or []
    utterances = state.get("utterances") or []
    enable_utt = state.get("params", {}).get("enable_utterances", True)
    pool = state.get("item_pool") or []
    lines: list[str] = []
    for i, p in enumerate(proposals):
        who = f"Player {int(p.get('player', 0)) + 1}"
        if p.get("accept"):
            lines.append(f"{who}: ACCEPTS")
            continue
        kept = p.get("items") or []
        if pool and len(pool) == len(kept):
            offered = [max(0, pool[j] - kept[j]) for j in range(len(pool))]
            lines.append(f"{who}: proposes keep={kept}, offer={offered}")
        else:
            lines.append(f"{who}: proposes keep={kept}")
        if enable_utt and i < len(utterances):
            symbols = utterances[i].get("symbols") or []
            lines.append(f"{who}: utters [{', '.join(str(s) for s in symbols)}]")
    return "\n".join(lines) if lines else "(empty)"

