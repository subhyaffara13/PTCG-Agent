
def propagate_shape_and_sharding(
    input_src_placements: Sequence[Placement],
    global_input_shape: Shape,
    rule: DimMap,
    mesh_sizes: Shape,
    strict_view: bool = False,
) -> tuple[Sequence[Placement], Sequence[Placement]]:
    """
    Determine input target sharding and output sharding based on
    given global tensor shape and input source sharding.

    Sharding propagation follows mapped dimensions:
    - An output dimension that maps directly to an input dimension is sharded equally
    - An output dimension that is a flattened set of input dimensions can be sharded:
      the first sharded dim stays as Shard, non-first sharded dims become _StridedShard
    - An output dimension that is a split of the input dimension can only be sharded
      if the leftmost split size is divisible by the mesh dimension
    """
    propagator = _ViewShardingPropagator(
        input_src_placements, global_input_shape, rule, mesh_sizes, strict_view
    )
    input_tgt_placements, input_to_output_tensor_dims = propagator.analyze()
    output_placements = propagator.rewrite_output_placements(
        input_tgt_placements, input_to_output_tensor_dims
    )
    return input_tgt_placements, output_placements

