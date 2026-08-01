
def _is_torch_distributed_initialized() -> bool:
    return (
        _torch_distributed_available
        and hasattr(torch.distributed, "is_initialized")
        and torch.distributed.is_initialized()
    )

