
def extract_tensor_metadata(t: torch.Tensor) -> tuple[Any, ...]:
    return (t.shape, t.stride(), t.dtype, t.device, t.requires_grad)


def extract_tensor_metadata(dynamic: bool, input: torch.Tensor) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    metadata["is_dynamic"] = dynamic

    assert isinstance(input, torch.Tensor)
    metadata["device_type"] = f"{input.device.type}"
    if is_cpu_device([input]):
        metadata["device_index"] = -1
    else:
        metadata["device_index"] = input.device.index
    metadata["dtype"] = f"{input.dtype}"
    metadata["sizes"] = list(input.size())
    metadata["strides"] = list(input.stride())
    metadata["requires_grad"] = input.requires_grad
    metadata["dispatch_key_set"] = torch._C._dispatch_keys(input).raw_repr()
    return metadata


def extract_tensor_metadata(t: Tensor) -> TensorMetadata:
    """
    Extract the TensorMetadata of a tensor.
    """
    memory_format = suggest_memory_format(t)
    # Don't call is_contiguous() on a Tensor which has symbolic sizes or things
    # will go badly (guards will be messed up?)
    if (
        t._has_symbolic_sizes_strides
        or is_sparse_any(t)
        or not t.is_contiguous(memory_format=memory_format)
    ):
        memory_format = None  # type: ignore[assignment]

    storage_offset = t.storage_offset()

    return TensorMetadata(
        t.dtype,
        t.shape,
        t.stride() if t.layout == torch.strided else (),
        t.device,
        t.layout,
        memory_format,
        storage_offset,
        # Only set storage_bytes for tensors that have storage (not sparse)
        t.untyped_storage().nbytes() if not is_sparse_any(t) else None,
        t.requires_grad,
        t.is_quantized,
        t.is_conj(),
        t.is_neg(),
        t.is_inference(),
        t.is_sparse,
        t.is_coalesced() if t.is_sparse else None,
        t.dense_dim() if is_sparse_any(t) else None,
        t.sparse_dim() if is_sparse_any(t) else None,
    )

