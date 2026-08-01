
def split_attention_implementation(implementation: str | None) -> tuple[bool, str | None]:
    """
    Split the optional `paged|` prefix from an attention implementation string.

    Note that `None` means using the default attention implementation, which is either torch's native `sdpa` or `eager` (if `sdpa` is not implemented for that model).
    """
    if implementation is None:
        return False, None

    is_paged = implementation.startswith("paged|")
    return is_paged, implementation.removeprefix("paged|")

