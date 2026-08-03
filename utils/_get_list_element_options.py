from typing import Any, List, Optional

def _get_list_element_options(field_annotation: Any) -> Optional[List[str]]:
    """
    Extract element options from List[Literal[...]] types
    """
    if (
        hasattr(field_annotation, "__origin__")
        and field_annotation.__origin__ is list
        and hasattr(field_annotation, "__args__")
    ):
        args = field_annotation.__args__
        if len(args) >= 1:
            element_type = args[0]
            return _extract_literal_values(element_type)
    return None

