
def _item_meta(a: TensorLikeType) -> FakeTensor:
    number_type = utils.dtype_to_type(a.dtype)
    return TensorMeta(number_type(-1))

