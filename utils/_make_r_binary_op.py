
def _make_r_binary_op(base_op):
    def rop(
        a: TensorLikeType | NumberType,
        b: TensorLikeType | NumberType,
    ) -> TensorLikeType:
        return base_op(b, a)

    return rop

