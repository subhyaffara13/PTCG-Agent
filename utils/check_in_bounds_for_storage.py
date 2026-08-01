
def check_in_bounds_for_storage(
    a: torch.TypedStorage, shape: ShapeType, strides: StrideType, storage_offset: int
):
    """
    Determines if the given shape, strides, and offset are valid for the given storage.
    """

    required_length = compute_required_storage_length(shape, strides, storage_offset)
    if a.size() < required_length:
        msg = (
            f"Can't view a storage of size {a.size()} with an offset of {storage_offset}, "
            f"shape of {str(shape)}, and strides of {str(strides)}, "
            f"which requires a storage of size {required_length}"
        )
        raise ValueError(msg)

