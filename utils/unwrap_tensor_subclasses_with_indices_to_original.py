from typing import Any

def unwrap_tensor_subclasses_with_indices_to_original(
    wrapped_args: list[Any],
) -> tuple[list[Any], list[int]]:
    ret_unwrapped = []
    ret_indices_to_original = []
    for i, a in enumerate(wrapped_args):
        a_unwrapped, _ = unwrap_tensor_subclasses(
            [a], [DummyAOTInput(9999)], append_symints=False
        )
        ret_unwrapped.extend(a_unwrapped)
        n = len(a_unwrapped)
        ret_indices_to_original.extend([i] * n)

    return ret_unwrapped, ret_indices_to_original

