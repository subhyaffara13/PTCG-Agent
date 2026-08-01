
def _create_tensor_from_params(
    *size, local_device, tensor_properties: TensorProperties
):
    """Helper to construct tensor from size, device and common params."""
    dtype = tensor_properties.dtype
    layout = tensor_properties.layout
    requires_grad = tensor_properties.requires_grad
    memory_format = tensor_properties.memory_format
    pin_memory = tensor_properties.pin_memory

    return torch.empty(
        *size,
        dtype=dtype,
        layout=layout,
        device=local_device,
        requires_grad=requires_grad,
        memory_format=memory_format,
        pin_memory=pin_memory,
    )

