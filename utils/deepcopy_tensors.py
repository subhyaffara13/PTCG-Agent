from typing import Any

def deepcopy_tensors(inputs: Any) -> Any:
    return pytree.tree_map_only(torch.Tensor, clone_input, inputs)

