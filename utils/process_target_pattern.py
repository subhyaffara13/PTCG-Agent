
def process_target_pattern(pattern: str) -> tuple[str, str | None]:
    """
    Process a target pattern for reverse mapping (when targets become sources).

    This handles several edge cases in checkpoint conversion mappings:
    - Removes `^` prefix and `$` suffix (start/end of string anchors)
    - Removes negative lookahead/lookbehind assertions
    - Detects capturing groups and replaces them with `\\1` backreference

    Args:
        pattern: The target pattern to process for reverse mapping.

    Returns:
        A tuple of (processed_pattern, captured_group) where captured_group is
        the original capturing group found (e.g., "(encoder|decoder)") or None.
    """
    # Some mapping contains `^` to notify start of string when matching -> remove it during reverse mapping
    pattern = pattern.removeprefix("^")
    # Some mapping contains `$` to notify end of string when matching -> remove it during reverse mapping
    pattern = pattern.removesuffix("$")
    # Remove negative lookahead/behind if any. This is ugly but needed for reverse mapping of
    # Qwen2.5, Sam3, Ernie4.5 VL MoE! It needs to be non greedy in case there are several
    pattern = re.sub(r"\(\?.+?\)?\)", "", pattern)
    # Remove the backslash for literal dots
    pattern = pattern.replace(r"\.", ".")
    # Allow capturing groups in patterns, i.e. to add/remove a prefix to all keys (e.g. timm_wrapper, sam3)
    capturing_group_match = re.search(r"\(.+?\)", pattern)
    captured_group = None
    if capturing_group_match:
        captured_group = capturing_group_match.group(0)
        pattern = pattern.replace(captured_group, r"\1", 1)
    return pattern, captured_group

