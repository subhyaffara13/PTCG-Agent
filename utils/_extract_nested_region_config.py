
def _extract_nested_region_config(fn):
    """
    Extract the NestedCompileRegionOptions from the HOP subgraph gm.meta["nested_region_config"]
    """
    gm_to_compile = None
    if isinstance(fn, torch.fx.GraphModule):
        gm_to_compile = fn
    elif isinstance(fn, FunctionalizeCtxWrapper):
        gm_to_compile = fn.subgraph

    if (
        isinstance(gm_to_compile, torch.fx.GraphModule)
        and hasattr(gm_to_compile, "meta")
        and "nested_region_config" in gm_to_compile.meta
    ):
        if isinstance(
            gm_to_compile.meta["nested_region_config"], NestedCompileRegionOptions
        ):
            return gm_to_compile.meta["nested_region_config"].decompositions
    return None

