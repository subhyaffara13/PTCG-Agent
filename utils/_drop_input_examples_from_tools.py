from typing import List, Optional

def _drop_input_examples_from_tools(
    tools: Optional[List[dict]],
) -> Optional[List[dict]]:
    if tools is None:
        return None
    cleaned_tools: List[dict] = []
    for tool in tools:
        if isinstance(tool, dict):
            cleaned_tools.append(_drop_input_examples_from_tool(tool))
        else:
            cleaned_tools.append(tool)
    return cleaned_tools

