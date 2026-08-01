
def _make_string_array(
    object: np.ndarray,
    dtype: DTypeLike | None = None,
    ndmin: int = 0,
    device: xc.Device | Sharding | None = None,
) -> Array:
  if not isinstance(object, np.ndarray):
    raise TypeError(
        "Currently, string arrays can only be made from NumPy"
        f" arrays. Got:  {type(object)}."
    )
  if dtype is not None and (
      (object.dtype == dtypes.string_dtype) != (dtype == dtypes.string_dtype)
  ):
    raise TypeError(
        f"Cannot make an array with dtype {dtype} from an object with dtype"
        f" {object.dtype}."
    )
  if ndmin > object.ndim:
    raise TypeError(
        f"ndmin {ndmin} cannot be greater than object's ndims"
        f" {object.ndim} for string arrays."
    )

  # Just do a device_put since XLA does not support string as a data type.
  return api.device_put(x=object, device=device)

