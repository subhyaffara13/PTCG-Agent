
def bitwise_same(ref: Any, res: Any, equal_nan: bool = False) -> bool:
    return same(
        ref,
        res,
        tol=0.0,
        equal_nan=equal_nan,
    )

