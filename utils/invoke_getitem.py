
def invoke_getitem(iinfo: IndexingInfo) -> Any:
    if iinfo.advanced_indexing:
        self_tensor = iinfo.self_tensor
        tup = slice_to_tuple(iinfo.flat_inputs)
        if self_tensor is None:
            raise RuntimeError("Cannot getitem on None tensor")
        rtensor = self_tensor[tup]
    else:
        rtensor = iinfo.self_tensor  # type: ignore[assignment]
        if rtensor is None:
            raise RuntimeError("Cannot getitem on None tensor")
        # rtensor is now guaranteed to be not None

    # Create a Tensor with the proper dimensions using the class method
    from . import Tensor

    return Tensor.from_positional(rtensor, iinfo.result_levels, iinfo.has_device)

