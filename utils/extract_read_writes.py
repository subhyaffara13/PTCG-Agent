
def extract_read_writes(
    fn: Callable[..., Any],
    *argsizes: Sequence[sympy.Expr],
    normalize: bool = False,
    prefix: str = "d",
    hidden_args: Sequence[list[sympy.Expr]] = (),
) -> ReadWrites:
    args, var_ranges = index_vars_squeeze(*argsizes, prefix=prefix)

    from .loop_body import LoopBody

    if isinstance(fn, LoopBody):
        inner = extract_loop_body_with_args(
            fn,
            [*args, *hidden_args],  # type: ignore[list-item]
            var_ranges,
            normalize,
        )
    else:
        # Slow path tracing the function
        rw = RecordLoadStore(var_ranges, normalize=normalize)
        with V.set_ops_handler(rw):
            fn(*args, *hidden_args)
        inner = rw.parent_handler

    if normalize:
        range_vars = []  # Number of vars could differ due to normalization
    else:
        range_vars = [*itertools.chain.from_iterable(args)]

    return ReadWrites(
        # pyrefly: ignore [missing-attribute]
        OrderedSet(inner._reads),
        # pyrefly: ignore [missing-attribute]
        OrderedSet(inner._writes),
        # pyrefly: ignore [missing-attribute]
        inner._index_exprs,
        range_vars,
        var_ranges,
    )

