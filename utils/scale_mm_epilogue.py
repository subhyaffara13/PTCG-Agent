
def scale_mm_epilogue():
    """
    Create an epilogue function that applies scaling to matrix multiplication result
    using the given scale factors.

    Args:
        dtype: The data type of the output
        scale_a: Scale factor for matrix A
        scale_b: Scale factor for matrix B

    Returns:
        Epilogue function that takes the accumulator and applies scaling
    """

    def epilogue(acc, inv_a_scale, inv_b_scale, bias=None):
        # The epilogue function receives the accumulator (result of mat1 @ mat2)
        # and applies the scaling factors
        # In the original scaled_mm, we use inverse scales, so we multiply by them
        mul_scales = V.ops.mul(inv_a_scale, inv_b_scale)
        mul_acc = V.ops.mul(acc, mul_scales)
        if bias is not None:
            return V.ops.add(mul_acc, bias)
        else:
            return mul_acc

    return epilogue

