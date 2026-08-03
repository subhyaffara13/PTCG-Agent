from typing import Any

def _map_to_rank_local_val(val: Any, rank: int) -> Any:
    if isinstance(val, LocalTensor):
        return val._local_tensors[rank]
    if isinstance(val, SymInt):
        if isinstance(val.node, LocalIntNode):
            return val.node._local_ints[rank]
        if isinstance(val.node, ConstantIntNode):
            return val.node.val
    return val

