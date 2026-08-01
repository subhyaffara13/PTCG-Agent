
def is_kernel(attn_implementation: str | None) -> bool:
    """Check whether `attn_implementation` matches a kernel pattern from the hub."""
    return (
        attn_implementation is not None
        and re.search(r"^[^/:]+/[^/:]+(?:@[^/:]+)?(?::[^/:]+)?$", attn_implementation) is not None
    )

