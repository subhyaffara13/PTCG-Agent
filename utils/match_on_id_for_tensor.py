
def match_on_id_for_tensor(guard: Guard) -> bool:
    source = guard.originating_source
    # For numpy tensors, always use TENSOR_MATCH because __from_numpy leads
    # to a new tensor every time and therefore id differs.
    if isinstance(source, NumpyTensorSource):
        return False

    if guard.is_specialized_nn_module():
        return True

    return source.is_dict_key() and not isinstance(source, GradSource)

