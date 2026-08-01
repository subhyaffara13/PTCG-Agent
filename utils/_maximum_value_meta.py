
def _maximum_value_meta(dtype: torch.dtype) -> FakeTensor:
    number_type = utils.dtype_to_type(dtype)
    return TensorMeta(number_type(-1))

