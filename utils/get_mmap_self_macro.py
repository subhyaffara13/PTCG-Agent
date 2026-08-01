
def get_mmap_self_macro(
    use_mmap_weights: bool, use_mmap_weights_external: bool
) -> list[str]:
    macros = []

    if use_mmap_weights and use_mmap_weights_external:
        raise RuntimeError(
            "Only one of use_mmap_weights and use_mmap_weights_external should be true"
        )
    if use_mmap_weights:
        macros.append(" USE_MMAP_SELF")
    elif use_mmap_weights_external:
        macros.append(" USE_MMAP_EXTERNAL")
    return macros

