
def _maybe_convert_to_dtype(a: TensorLikeType, dtype: torch.dtype) -> TensorLikeType:
    pass


def _maybe_convert_to_dtype(a: NumberType, dtype: torch.dtype) -> NumberType:
    pass


def _maybe_convert_to_dtype(a: Sequence, dtype: torch.dtype) -> Sequence:
    pass


def _maybe_convert_to_dtype(a: None, dtype: torch.dtype) -> None:
    pass


def _maybe_convert_to_dtype(a, dtype):
    if isinstance(a, TensorLike):
        if a.dtype != dtype:
            return a.to(dtype)
        return a
    if isinstance(a, Number):
        return utils.dtype_to_type_ctor(dtype)(a)  # type: ignore[arg-type]
    if isinstance(a, Sequence):
        return tuple(_maybe_convert_to_dtype(x, dtype) for x in a)
    # Passthrough None because some functions wrapped with type promotion
    # wrapper might have optional args
    if a is None:
        return None

    raise ValueError(
        f"Received unsupported type {type(a)}. Expected TensorLike, Number, or Sequence."
    )

