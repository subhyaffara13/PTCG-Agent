from typing import Any, Dict, List, Optional, Union

def _augment_system_with_summary(
    system: Optional[Union[str, List[Dict[str, Any]]]],
    summary_text: str,
) -> Union[str, List[Dict[str, Any]]]:
    """Prepend a "Previous conversation summary: ..." block to ``system``."""
    prefix = f"{COMPACT_SUMMARY_SYSTEM_PREFIX}{summary_text}\n\n"
    if system is None:
        return prefix.rstrip()
    if isinstance(system, str):
        return f"{prefix}{system}"
    # List of content blocks: prepend the prefix to the first text block,
    # otherwise insert a new text block at the head.
    for idx, block in enumerate(system):
        if isinstance(block, dict) and block.get("type") == "text":
            existing = block.get("text", "") or ""
            new_block = {**block, "text": f"{prefix}{existing}"}
            return [*system[:idx], new_block, *system[idx + 1 :]]
    return [{"type": "text", "text": prefix.rstrip()}, *system]

