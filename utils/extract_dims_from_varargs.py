
def extract_dims_from_varargs(
    dims: DimsSequenceType | tuple[DimsSequenceType, ...],
) -> DimsSequenceType:
    if dims and isinstance(dims[0], Sequence):
        if len(dims) != 1:
            raise AssertionError(
                f"Expected exactly 1 element in dims when first element is a Sequence, got {len(dims)}"
            )
        dims = cast(tuple[DimsSequenceType], dims)
        return dims[0]
    else:
        return cast(DimsSequenceType, dims)

