
def maybe_skip_decompose(aot_config: AOTConfig) -> Generator[None, None, None]:
    old_decomp = aot_config.decompositions
    try:
        if config.selective_decompose:
            aot_config.decompositions = {}
        yield
    finally:
        aot_config.decompositions = old_decomp

