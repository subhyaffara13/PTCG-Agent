from typing import Any

def host_memory_stats_as_nested_dict() -> dict[str, Any]:
    r"""Return the result of :func:`~torch.cuda.host_memory_stats` as a nested dictionary."""
    if not is_initialized():
        return {}
    return torch._C._cuda_hostMemoryStats()

