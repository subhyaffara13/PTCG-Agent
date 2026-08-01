
def extract_free_symbols(
    fn: Callable[..., Any],
    index: Sequence[sympy.Expr],
    rindex: Sequence[sympy.Expr] | None = None,
    unbacked_only: bool = True,
) -> OrderedSet[sympy.Symbol]:
    from .ir import FlexibleLayout

    args = [index, rindex] if rindex is not None else [index]
    handler = FreeSymbolsOpsHandler(unbacked_only)
    # NB: I cargo culted the allow_indexing patch here, I don't understand why
    # people do this all over
    with (
        V.set_ops_handler(handler),
        patch.object(FlexibleLayout, "allow_indexing", True),
    ):
        fn(*args)
    return handler.symbols

