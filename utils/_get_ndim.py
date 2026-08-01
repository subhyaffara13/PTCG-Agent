
def _get_ndim(tensor_meta: Any) -> int:
    if not isinstance(tensor_meta, TensorMeta):
        raise AssertionError(f"Expected TensorMeta, got {type(tensor_meta)}")
    return len(tensor_meta.shape)

