
def freezing_passes(gm: torch.fx.GraphModule, aot_example_inputs):
    """
    Passes that are applied to the graph to freeze pass.
    """

    from ..freezing import constant_fold

    lazy_init()
    # We need a few rounds of binary folding to get rid of all the
    # unnecessary nodes, but may need a good method to chose the rounds number.
    # works like: conv+binary+binary.
    binary_folding = counters["inductor"]["binary_folding"]
    fake_tensor_prop(gm, aot_example_inputs, True)

    torch._inductor.fx_passes.binary_folding.mark_mixed_dtype_allowed_computation_ops(
        gm
    )
    for _ in range(4):
        constant_fold(gm)
        # Make sure meta['val'] is properly set for all nodes
        fake_tensor_prop(gm, aot_example_inputs, True)
        binary_folding_pass.apply(gm.graph)  # type: ignore[arg-type]
        # If we don't have binary folding, we don't need to run the pass again.
        # TODO: remove the need to run fake_tensor_prop on the whole model.
        if counters["inductor"]["binary_folding"] == binary_folding:
            break
        binary_folding = counters["inductor"]["binary_folding"]

    torch._inductor.fx_passes.binary_folding.recover_original_precision_folded_computation_ops(
        gm
    )

    constant_fold(gm)
    fake_tensor_prop(gm, aot_example_inputs, True)

    for pattern in pass_patterns:
        pattern.apply(gm.graph)  # type: ignore[arg-type]

    # The CPU weight packing always assume the conv's weight is channels last,
    # So make sure the layout_optimization is on when doing it.
    if (
        torch._C._has_mkldnn
        and config.cpp.weight_prepack
        and config.layout_optimization
    ):
        from .mkldnn_fusion import _eliminate_duplicate_packed_nodes

        _eliminate_duplicate_packed_nodes(gm)

    stable_topological_sort(gm.graph)
    gm.recompile()
    gm.graph.lint()

