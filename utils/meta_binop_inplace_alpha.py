
def meta_binop_inplace_alpha(self, other, alpha=1):
    """
    Some checks for inplace ops.
    Checks for promotion rules for some dtypes.
    int.add/sub_(float) and bool.add/sub_(others) are rejected.
    Promoting in these in-place operations would require reallocating
    and copying over elements, hence not allowed.
    Checks for alpha param.
    """

    def is_integeric(arg):
        if isinstance(arg, TensorLike):
            return utils.is_integer_dtype(arg.dtype)
        else:
            return isinstance(arg, IntLike)

    def is_floatic(arg):
        if isinstance(arg, TensorLike):
            return utils.is_float_dtype(arg.dtype)
        else:
            return isinstance(arg, FloatLike)

    def is_booleanic(arg):
        if isinstance(arg, TensorLike):
            return utils.is_boolean_dtype(arg.dtype)
        else:
            return isinstance(arg, BoolLike)

    # Do not allow int+float->int in-place
    if is_integeric(self) and is_floatic(other):
        raise RuntimeError(
            "Promotion of int.add/sub_(float) in in-place ops are not possible due to element size change."
        )

    # Do not allow bool+other->bool in-place
    if is_booleanic(self) and not is_booleanic(other):
        raise RuntimeError(
            "Promotion of book.add/sub_(others) in in-place ops are not possible due to element size change."
        )

    if isinstance(other, torch.Tensor):
        check_inplace_broadcast(self.shape, other.shape)
    return self

