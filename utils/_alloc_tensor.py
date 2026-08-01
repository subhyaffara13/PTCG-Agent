
def _alloc_tensor(
    props: TensorProperties, size: Sequence[int], device_type: str = "cuda"
) -> torch.Tensor:
    if device_type == "cpu":
        device = cast(torch.device, _get_device_module(device_type).current_device())
    else:
        device = torch.device(
            device_type, _get_device_module(device_type).current_device()
        )

    return torch.empty(
        size=size,
        dtype=props.dtype,
        layout=props.layout,
        requires_grad=props.requires_grad,
        pin_memory=props.pin_memory,
        device=device,
    )

