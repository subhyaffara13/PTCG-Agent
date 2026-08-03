from typing import Dict, List, Optional

def branch(
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    size_dict: Dict[str, int],
    memory_limit: Optional[int] = None,
    nbranch: Optional[int] = None,
    cutoff_flops_factor: int = 4,
    minimize: str = "flops",
    cost_fn: str = "memory-removed",
) -> PathType:
    optimizer = BranchBound(
        nbranch=nbranch, cutoff_flops_factor=cutoff_flops_factor, minimize=minimize, cost_fn=cost_fn
    )
    return optimizer(inputs, output, size_dict, memory_limit)

