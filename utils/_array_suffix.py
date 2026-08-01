
def _array_suffix(array_format: ArrayFormat, array_index: int) -> str:
    if array_format == "brackets":
        return "[]"
    if array_format == "indices":
        return f"[{array_index}]"
    if array_format == "repeat" or array_format == "comma":
        # Both repeat the bare field name for each file part; there is no
        # meaningful way to comma-join binary parts.
        return ""
    raise NotImplementedError(
        f"Unknown array_format value: {array_format}, choose from {', '.join(get_args(ArrayFormat))}"
    )

