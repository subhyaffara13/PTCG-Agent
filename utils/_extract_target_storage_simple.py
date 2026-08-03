from typing import Optional

def _extract_target_storage_simple(target_storage_form: Optional[str] = None) -> str:
    """
    Extract target_storage parameter from form field.

    Args:
        target_storage_form: target_storage from form field

    Returns:
        str: Target storage backend name, or "default"
    """
    if target_storage_form:
        return target_storage_form.strip()
    return "default"

