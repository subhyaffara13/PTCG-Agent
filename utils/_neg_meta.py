
def _neg_meta(a: TensorLikeType):
    torch._check(
        a.dtype is not torch.bool,
        lambda: (
            "Negation, the `-` operator, on a bool tensor is not supported. "
            "If you are trying to invert a mask, use the `~` or `logical_not()` "
            "operator instead."
        ),
    )

