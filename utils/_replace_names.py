import re

def _replace_names(shape_expr: str, rename_mapping: dict[str, str]) -> str:
    """Replace all known names in a shape expression with new names."""
    for old_name, new_name in rename_mapping.items():
        shape_expr = re.sub(
            rf"(?<!\w){re.escape(old_name)}(?!\w)", new_name, shape_expr
        )
    return shape_expr

