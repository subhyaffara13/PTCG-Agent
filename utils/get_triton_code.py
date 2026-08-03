from typing import Callable

def get_triton_code(fn: Callable[P, _T], *args: P.args, **kwargs: P.kwargs) -> str:
    # pyrefly: ignore [bad-argument-type]
    source_codes = get_code(fn, *args, **kwargs)
    # Can have two outputs if backwards was eagerly compiled
    assert 1 <= len(source_codes) <= 2, (
        f"expected one or two code outputs got {len(source_codes)}"
    )
    return source_codes[0]

