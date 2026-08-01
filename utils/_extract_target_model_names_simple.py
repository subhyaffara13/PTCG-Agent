
def _extract_target_model_names_simple(
    target_model_names_form: Optional[str] = None,
) -> List[str]:
    """
    Extract target_model_names parameter from form field.
    """
    if not target_model_names_form:
        return []

    # Parse comma-separated string into list
    if isinstance(target_model_names_form, str):
        return [
            name.strip() for name in target_model_names_form.split(",") if name.strip()
        ]
    elif isinstance(target_model_names_form, list):
        return [str(name).strip() for name in target_model_names_form if name]

    return []

