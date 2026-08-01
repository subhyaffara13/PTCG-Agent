
def _get_torch_distributed_world_size() -> int:
    if not _is_torch_distributed_initialized() or not hasattr(torch.distributed, "get_world_size"):
        return 1
    return torch.distributed.get_world_size()

