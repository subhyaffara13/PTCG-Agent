from typing import Any, Dict

def _write_dict_to_shared_memory(
    space: Dict, index: int, values: dict[str, Any], shared_memory
):
    for key, subspace in space.spaces.items():
        write_to_shared_memory(subspace, index, values[key], shared_memory[key])


def _write_dict_to_shared_memory(space, index, values, shared_memory):
    for key, subspace in space.spaces.items():
        write_to_shared_memory(subspace, index, values[key], shared_memory[key])

