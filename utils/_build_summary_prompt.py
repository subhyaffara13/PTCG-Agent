from typing import Any, Dict, List, Optional

def _build_summary_prompt(
    edit_spec: Dict[str, Any], tools: Optional[List[Dict[str, Any]]]
) -> str:
    custom = edit_spec.get("instructions")
    if isinstance(custom, str) and custom.strip():
        return custom
    prompt = COMPACT_DEFAULT_INSTRUCTIONS
    if tools:
        prompt = f"{prompt}{COMPACT_NO_TOOL_CALLS_SUFFIX}"
    return prompt

