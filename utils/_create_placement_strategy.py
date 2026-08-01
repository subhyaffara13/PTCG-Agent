
def _create_placement_strategy(
    node: Node,
    mesh: DeviceMesh,
    placements: tuple[Placement, ...],
    input_specs: Sequence[DTensorSpec] | None = None,
) -> OpSpec:
    """
    Util function to construct an OpSpec for a given node.
    """
    placement = OpSpec(
        input_specs=input_specs,
        output_specs=DTensorSpec(
            mesh=mesh,
            placements=placements,
        ),
    )
    _populate_tensor_meta(node, placement.output_specs)
    return placement

