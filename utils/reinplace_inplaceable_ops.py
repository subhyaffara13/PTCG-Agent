
def reinplace_inplaceable_ops(
    fake_tensor_updater: torch._inductor.fx_utils.FakeTensorUpdater,
    graph: torch.fx.Graph,
) -> None:
    with enable_python_dispatcher():
        canonicalize_view_scatter_ops(graph)
        # canonicalize_view_scatter_ops adds new operations to the graph.
        # We run fake_tensor_updater to update the alias information.
        # Correct alias information is required for `reinplace_inplaceable_ops_core`.
        fake_tensor_updater.incremental_update()
        reinplace_inplaceable_ops_core(graph)
        decompose_generalized_scatter(graph)

