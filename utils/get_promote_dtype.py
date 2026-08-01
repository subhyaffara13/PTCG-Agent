
def get_promote_dtype(args):
    return (
        # pyrefly: ignore [no-matching-overload]
        functools.reduce(
            torch.promote_types,  # type: ignore[arg-type]
            # pyrefly: ignore [bad-argument-type]
            [n.dtype for n in args if isinstance(n, CppCSEVariable)],
        )
        if all(n.dtype is not None for n in args if isinstance(n, CppCSEVariable))
        else None  # not enough info to calculate the promote dtype
    )

