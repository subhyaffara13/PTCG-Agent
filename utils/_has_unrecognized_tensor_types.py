
def _has_unrecognized_tensor_types(types: Sequence[type]) -> bool:
    unrecognized_types = [
        t
        for t in types
        if t not in (torch.Tensor, torch._subclasses.FakeTensor, FunctionalTensor)
    ]
    if unrecognized_types:
        not_implemented_log.debug(
            "FunctionalTensor unrecognized subclass(es): %s", unrecognized_types
        )
    return bool(unrecognized_types)

