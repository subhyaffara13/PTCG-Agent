
def _get_torch_cpp_wrapper_definition() -> list[str]:
    defs = ["TORCH_INDUCTOR_CPP_WRAPPER", "STANDALONE_TORCH_HEADER"]
    if config.cpp_cache_precompile_headers:
        defs.append("TORCH_INDUCTOR_PRECOMPILE_HEADERS")
    return defs

