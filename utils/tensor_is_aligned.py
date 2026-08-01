
def tensor_is_aligned(tensor: torch.Tensor) -> bool:
    # See Note: [Input Alignment handling in Inductor]
    # Right now, we don't try to guard on the alignment of the storage offset.
    # When this comment was written, non-symbolic storage_offsets are not guarded on
    # but symbolic storage_offsets are. For consistency, we suppress guard creation
    # upon performing this check: that ensures that we don't add recompiles when we
    # add this logic.
    from torch.fx.experimental.symbolic_shapes import statically_known_true

    return statically_known_true(
        (tensor.storage_offset() * get_dtype_size(tensor.dtype)) % GPU_ALIGN_BYTES == 0
    )

