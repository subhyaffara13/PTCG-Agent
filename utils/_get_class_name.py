
def _get_class_name(model_class: str | list[str]):
    if isinstance(model_class, list | tuple):
        return " or ".join([f"[`{c}`]" for c in model_class if c is not None])
    return f"[`{model_class}`]"

