
def get_tensor_symint(tensor, *, coeff=1):
    from torch._subclasses.fake_tensor import FakeTensor
    from torch._subclasses.functional_tensor import mb_unwrap_functional_tensor

    # NB: Only FakeTensor is associated with a memo
    tensor = mb_unwrap_functional_tensor(tensor)
    if isinstance(tensor, FakeTensor):
        return tensor.get_nested_int(coeff=coeff)

    global _tensor_id_counter

    tensor_symint = _tensor_symint_registry.get(tensor)
    if tensor_symint is None:
        tensor_symint = torch.SymInt(NestedIntNode(_tensor_id_counter, coeff))
        _tensor_id_counter += 1
        _tensor_symint_registry[tensor] = tensor_symint
    return tensor_symint

