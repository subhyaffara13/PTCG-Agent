
def process_source_pattern(source_pattern: str, target_pattern: str) -> str:
    """
    Process a source pattern for reverse mapping (when sources become targets).
    This is useful because usually if the original source (so now the target in reverse mode) had a `^` or `$`
    to restrict to start/end of string, we should do the same in reverse mode. This is why this method in conditioned
    on the target pattern, we want to do it only for pairs (source, target) when the original source (so the current target
    in reverse mode) had it.
    """
    if target_pattern.startswith("^"):
        source_pattern = f"^{source_pattern}" if not source_pattern.startswith("^") else source_pattern
    if target_pattern.endswith("$"):
        source_pattern = f"{source_pattern}$" if not source_pattern.endswith("$") else source_pattern

    return source_pattern

