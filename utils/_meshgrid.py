
def _meshgrid(*tensors, indexing: str | None):
    if has_torch_function(tensors):
        return handle_torch_function(meshgrid, tensors, *tensors, indexing=indexing)
    if len(tensors) == 1 and isinstance(tensors[0], (list, tuple)):
        # the old interface of passing the operands as one list argument
        tensors = tensors[0]  # type: ignore[assignment]

    # Continue allowing call of old method that takes no indexing
    # kwarg for forward compatibility reasons.
    #
    # Remove this two weeks after landing.
    kwargs = {} if indexing is None else {"indexing": indexing}
    return _VF.meshgrid(tensors, **kwargs)  # type: ignore[attr-defined]

