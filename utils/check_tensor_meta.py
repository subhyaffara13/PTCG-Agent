
def check_tensor_meta(
    local_tensor, check_shape_stride=False
) -> Optional["dtensor_spec.TensorMeta"]:
    local_metadata = {
        "dtype": local_tensor.dtype,
        "requires_grad": local_tensor.requires_grad,
    }

    if check_shape_stride:
        local_metadata.update(
            {"shape": local_tensor.shape, "stride": local_tensor.stride()}
        )

    gathered_metadata = [None for _ in range(torch.distributed.get_world_size())]
    torch.distributed.all_gather_object(gathered_metadata, local_metadata)

    # Check if metadata is consistent across ranks
    if not all(meta == local_metadata for meta in gathered_metadata):
        raise ValueError(
            "Inconsistent tensor metadata (including shape and stride) across ranks."
        )
    return None

