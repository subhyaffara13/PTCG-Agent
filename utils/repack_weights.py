
def repack_weights(
    packed_parameter: torch.Tensor,
    sharded_dim: int,  # The dimension index in the global tensor that was sharded
    world_size: int,
    num_blocks: int = 2,
) -> torch.Tensor:
    """
    Reorders a tensor that was reconstructed from sharded packed weights into its canonical packed format.

    For example, if a weight was packed (e.g., gate_proj and up_proj) and then sharded,
    DTensor.full_tensor() might produce an interleaved layout like [G0, U0, G1, U1, ...]
    along the sharded dimension. This function reorders it to [G0, G1, ..., U0, U1, ...].
    This is an inverse operation to get_packed_weights.

    Args:
        reconstructed_tensor: The tensor reconstructed from DTensor (e.g., via .full_tensor().contiguous()).
        sharded_dim: The dimension index in the reconstructed_tensor that was originally sharded.
        world_size: The tensor parallel world size.
        num_packed_projs: The number of projections that were packed together (e.g., 2 for gate_up_proj).

    Returns:
        The reordered tensor in canonical packed format.
    """

    if num_blocks != 2:
        raise ValueError(
            "Num blocks different from 2 is not supported yet. This is most likely a bug in your implementation as we only pack gate and up projections together."
        )

    actual_sharded_dim = sharded_dim if sharded_dim >= 0 else sharded_dim + packed_parameter.ndim
    total_size_on_sharded_dim = packed_parameter.shape[actual_sharded_dim]
    original_block_size_on_dim = total_size_on_sharded_dim // num_blocks
    shard_chunk_size = original_block_size_on_dim // world_size

    prefix_shape = packed_parameter.shape[:actual_sharded_dim]
    suffix_shape = packed_parameter.shape[actual_sharded_dim + 1 :]

    tensor_view = packed_parameter.view(
        *prefix_shape,
        world_size,
        num_blocks,
        shard_chunk_size,
        *suffix_shape,
    )

    # Permute to bring num_packed_projs first, then world_size, then shard_chunk_size
    # This groups all chunks of G together, then all chunks of U together.
    # Target order of these middle dimensions: (num_packed_projs, world_size, shard_chunk_size)
    # Current order of view's middle dimensions: (world_size, num_packed_projs, shard_chunk_size)
    # Absolute indices of the dimensions to be permuted (world_size, num_packed_projs)
    axis_ws_abs = len(prefix_shape)
    axis_npp_abs = len(prefix_shape) + 1

    permute_order = list(range(tensor_view.ndim))
    permute_order[axis_ws_abs], permute_order[axis_npp_abs] = permute_order[axis_npp_abs], permute_order[axis_ws_abs]

    tensor_permuted = tensor_view.permute(*permute_order)

    # Reshape back to the original tensor's ndim, with the sharded dimension now correctly ordered as [G_all, U_all].
    # The final shape should be the same as reconstructed_tensor.
    final_ordered_tensor = tensor_permuted.reshape_as(packed_parameter)

    return final_ordered_tensor

