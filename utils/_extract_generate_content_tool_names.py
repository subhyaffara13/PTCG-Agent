from typing import List

def _extract_generate_content_tool_names(data: dict) -> List[str]:
    """Google generateContent: tools[].functionDeclarations[].name"""
    names: List[str] = []
    for tool in data.get("tools") or []:
        if not isinstance(tool, dict):
            continue
        for decl in tool.get("functionDeclarations") or []:
            if isinstance(decl, dict) and decl.get("name"):
                names.append(str(decl["name"]))
    return names

