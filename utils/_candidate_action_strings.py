from typing import Any

def _candidate_action_strings(payload: dict[str, Any]) -> list[str]:
    """Convert a parsed JSON dict into candidate legal-action strings."""
    candidates: list[str] = []
    action = str(payload.get("action", "")).strip().lower() if payload.get("action") else ""

    if action == "accept" or payload.get("accept") is True:
        candidates.append("Proposal: Agreement reached!")
        return candidates

    # Proposal: items either at "keep", "items", or top-level list.
    keep = payload.get("keep") or payload.get("items") or payload.get("proposal")
    items = _parse_int_list(keep)
    if items is not None and action in ("", "propose", "proposal"):
        candidates.append(f"Proposal: [{', '.join(str(i) for i in items)}]")

    # Utterance: "symbols" or "utterance" key.
    symbols = payload.get("symbols") or payload.get("utterance")
    syms = _parse_int_list(symbols)
    if syms is not None:
        candidates.append(f", Utterance: [{', '.join(str(i) for i in syms)}]")

    return candidates

