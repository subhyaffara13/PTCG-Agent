
def _get_extension_dir(short_name: str) -> Path:
    safe_name = _validate_extension_short_name(short_name, original_input=short_name)
    root = _get_extensions_root().resolve()
    target = (root / f"hf-{safe_name}").resolve()
    if root not in target.parents:
        raise CLIError(f"Invalid extension name '{short_name}'.")
    return target

