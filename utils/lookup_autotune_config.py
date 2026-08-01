
def lookup_autotune_config(size_hints, fn) -> Config | None:
    lookup_table = torch._inductor.config.autotune_lookup_table
    cached_config = None
    if len(lookup_table) > 0 and "_fused_" in fn.src:
        fn_hash = generate_lookup_hash_from_source_code(str(size_hints), fn.src)
        if fn_hash in lookup_table:
            config_dict = lookup_table[fn_hash]
            block_configs = {k: v for k, v in config_dict.items() if "BLOCK" in k}
            cached_config = Config(
                block_configs,
                num_warps=config_dict["num_warps"],
                num_stages=config_dict["num_stages"],
            )

    return cached_config

