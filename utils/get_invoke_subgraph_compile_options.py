
def get_invoke_subgraph_compile_options(
    inductor_config_patches=None,
    decompositions=None,
    partitioner="min_cut_rematerialization_partition",
):
    if inductor_config_patches is None:
        inductor_config_patches = {"triton.autotune_at_compile_time": True}
    inductor_compile = functools.partial(
        invoke_subgraph_inductor_compile,
        inductor_config_patches=inductor_config_patches,
    )

    if inductor_config_patches:
        from torch._inductor import config as inductor_config

        # Validate that all config keys exist
        for key in inductor_config_patches:
            if not hasattr(inductor_config, key):
                raise ValueError(
                    f"Invalid inductor config key '{key}' in get_invoke_subgraph_compile_options. "
                    f"Available config keys can be found in torch._inductor.config"
                )

    return NestedCompileRegionOptions(
        fw_compiler=inductor_compile,
        bw_compiler=inductor_compile,
        partitioner=partitioner,
        decompositions=decompositions,
    )

