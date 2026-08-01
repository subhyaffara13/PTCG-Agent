
def _get_tid(tensor: torch.Tensor) -> _TID:
    # FIXME: This is almost definitely a bug.
    if isinstance(
        tensor,
        (
            torch._subclasses.fake_tensor.FakeTensor,
            torch._subclasses.functional_tensor.FunctionalTensor,
        ),
    ):
        data_ptr = 0
    else:
        data_ptr = tensor.data_ptr()
    return (id(tensor), data_ptr, tensor._version)

