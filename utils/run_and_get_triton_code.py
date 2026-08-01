
def run_and_get_triton_code(
    fn: Callable[P, _T], *args: P.args, **kwargs: P.kwargs
) -> str:
    # pyrefly: ignore [bad-argument-type]
    _, source_codes = run_and_get_code(fn, *args, **kwargs)
    # Can have two outputs if backwards was eagerly compiled
    assert 1 <= len(source_codes) <= 2, (
        f"expected one or two code outputs got {len(source_codes)}"
    )
    return source_codes[0]

