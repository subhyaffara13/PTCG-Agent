from typing import Optional

def _namespace_element_name(tag_name: str, xmlns: Optional[str]) -> str:
    if tag_name.startswith('{'):
        return tag_name
    if xmlns:
        return f'{{{xmlns}}}{tag_name}'
    return tag_name

