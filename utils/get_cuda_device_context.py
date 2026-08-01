
def get_cuda_device_context(gm: torch.fx.GraphModule) -> AbstractContextManager[None]:
    """
    Returns a cuda device context manager if there is a single device in the graph
    """
    if not torch.cuda.is_available():
        return contextlib.nullcontext()

    cuda_devices: OrderedSet[torch.device] = OrderedSet(
        device for device in get_all_devices(gm) if device.type == "cuda"
    )

    return (
        torch.cuda.device(next(iter(cuda_devices)))  # type: ignore[return-value]
        if len(cuda_devices) == 1
        else contextlib.nullcontext()
    )

