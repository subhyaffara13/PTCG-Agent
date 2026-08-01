
def _is_plain_tensor(t: object) -> bool:
    return (
        type(t) is Tensor
        and t.layout == torch.strided
        and not (
            t.is_sparse
            or t.is_nested
            or is_functorch_wrapped_tensor(t)
            or is_legacy_batchedtensor(t)
            or torch._is_functional_tensor(t)
        )
    )

