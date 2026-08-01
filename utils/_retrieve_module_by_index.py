
def _retrieve_module_by_index(nn_module_index: int) -> torch.nn.Module:
    # Check make_fx storage first (used by _invoke_leaf_function_python).
    # Fall back to the Dynamo retriever (used by the compiled path).
    if nn_module_index in _makefx_module_storage:
        if nn_module_index >= 0:
            raise RuntimeError(
                f"Expected negative nn_module_index for non-strict trace over leaf_function, but got {nn_module_index}."
            )
        return _makefx_module_storage[nn_module_index]

    if _leaf_function_module_retriever is None:
        raise RuntimeError("Leaf function module retriever not set.")

    mod = _leaf_function_module_retriever(nn_module_index)
    if not isinstance(mod, torch.nn.Module):
        raise TypeError(
            f"Expected nn.Module at index {nn_module_index} for leaf function invocation, "
            f"but got {type(mod).__name__}."
        )
    return mod

