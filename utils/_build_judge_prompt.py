from typing import Any, Dict, List

def _build_judge_prompt(
    criteria: List[Dict[str, Any]],
    messages: List[Dict[str, Any]],
    response_text: str,
) -> str:
    criteria_block = "\n".join(
        f'- {c.get("name", "")} (weight {c.get("weight", 0)}%): {c.get("description", "")}'
        for c in criteria
    )
    conversation = "\n".join(
        f'{m.get("role", "user").upper()}: {_extract_text_from_content(m.get("content", ""))}'
        for m in messages
        if m.get("content") is not None
    )
    return (
        f"Criteria to evaluate:\n{criteria_block}\n\n"
        f"Conversation:\n{conversation}\n\n"
        f"Assistant response to evaluate:\n{response_text}"
    )

