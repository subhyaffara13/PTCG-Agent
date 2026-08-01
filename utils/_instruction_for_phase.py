
def _instruction_for_phase(phase: str | None, legal_strings: Sequence[str]) -> str:
    if phase and phase in _PHASE_INSTRUCTION:
        return _PHASE_INSTRUCTION[phase]
    # Fallback: infer from the legal moves on offer.
    legals = set(legal_strings)
    if "Draw upcard" in legals or "Draw stock" in legals:
        return _PHASE_INSTRUCTION["Draw"]
    if "Knock" in legals and any(_CARD_RE.fullmatch(s) for s in legals):
        return _PHASE_INSTRUCTION["Discard"]
    if "Pass" in legals and "Draw upcard" not in legals:
        return _PHASE_INSTRUCTION["Layoff"]
    return (
        "Choose a legal action for this phase. Use an exact OpenSpiel "
        "action string."
    )

