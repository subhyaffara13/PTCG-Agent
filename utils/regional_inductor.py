
def regional_inductor(gm, *example_args):
    """
    Scoops out inductor marked regions and compiles them with inductor.

    Inductor options should be provided via the annotation API::

        with fx_traceback.annotate(
            {
                "compile_with_inductor": {
                    "inductor_configs": {
                        "max_autotune": True,
                        "triton.cudagraphs": False,
                    }
                }
            }
        ):
            ...
    """

    # fuser utils create new nodes using create_proxy which retains the seq_nr
    # metadata and cause issues

    with torch.fx.traceback.preserve_node_meta(enable=False):
        gm = _create_inductor_marked_regions(gm)
        gm = _compile_inductor_marked_regions(gm)
        if torch._functorch.config.force_autograd_cache:
            from torch._inductor.output_code import RegionalOutputCode

            gm = RegionalOutputCode(gm)
        return gm

