
def _torch_to_device(
    x: torch.Tensor,
    device: torch.device | str | int,
    /,
    stream: int | Any | None = None,
) -> torch.Tensor:
    if stream is not None:
        raise NotImplementedError
    return x.to(device)

