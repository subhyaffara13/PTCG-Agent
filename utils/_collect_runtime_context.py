
def _collect_runtime_context(
    selection: SelectedRuntimeContext | bool,
) -> dict[str, object] | None:
    """Collect runtime context based on selection.

    Args:
        selection: True to include all, False to exclude all, or a dict
                  specifying which forms to include.

    Returns:
        Dictionary of selected context data, or None if excluded.
    """
    return {
        form: getattr(_RuntimeContext, form)()
        for form in _RuntimeContext.forms_of_context()
        if selection is True or (selection and selection.get(form, False))
    } or None

