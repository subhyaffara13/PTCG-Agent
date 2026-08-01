
def _normalize_extension_name(name: str) -> str:
    candidate = name.strip()
    if not candidate:
        raise CLIError("Extension name cannot be empty.")
    normalized = candidate[3:] if candidate.startswith("hf-") else candidate
    return _validate_extension_short_name(normalized, original_input=name)

