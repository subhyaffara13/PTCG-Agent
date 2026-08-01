
def template(pattern, flags=0):
    "Compile a template pattern, returning a pattern object."
    return _compile(pattern, flags | TEMPLATE, False, {}, False)


def template(
    num_stages,
    num_warps,
    triton_meta,
    num_consumer_groups=0,
    num_buffers_warp_spec=0,
    filename=None,
    inductor_meta=None,
    **kwargs,
):
    """
    Compile a triton template
    """
    # Prepare the base configuration
    config_args = {
        "num_stages": num_stages,
        "num_warps": num_warps,
    }

    # Conditionally add arguments based on HAS_WARP_SPEC
    if HAS_WARP_SPEC:
        config_args.update(
            {
                "num_consumer_groups": num_consumer_groups,
                "num_buffers_warp_spec": num_buffers_warp_spec,
            }
        )

    for k in tlx_only_cuda_options():
        if v := triton_meta.get(k, None):
            config_args[k] = v

    return cached_autotune(
        None,
        [triton.Config({}, **config_args)],
        triton_meta=triton_meta,
        inductor_meta=inductor_meta,
        heuristic_type=HeuristicType.TEMPLATE,
        filename=filename,
    )

