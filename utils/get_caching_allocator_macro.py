
def get_caching_allocator_macro() -> list[str]:
    from torch._inductor import config

    macros = []
    if config.aot_inductor.weight_use_caching_allocator:
        macros.append(" AOT_INDUCTOR_USE_CACHING_ALLOCATOR")
    return macros

