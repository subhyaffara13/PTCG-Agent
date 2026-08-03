import re
from typing import Callable

def run_and_get_kernels(
    fn: Callable[P, _T], *args: P.args, **kwargs: P.kwargs
) -> tuple[_T, list[str]]:
    remove_quote = kwargs.pop("remove_quote", False)
    # pyrefly: ignore [bad-argument-type]
    result, source_codes = run_and_get_code(fn, *args, **kwargs)
    kernels = []
    for code in source_codes:
        if config.cpp_wrapper and config.triton.autotune_at_compile_time is not True:
            # With lazy Triton kernel compilation, kernel sources are embedded
            # inside C++ R"TRITON(...)TRITON" raw strings.
            kernels.extend(re.findall(r'R"TRITON\((.*?)\)TRITON"', code, re.DOTALL))
        else:
            kernels.extend(re.findall(r"'''.*?'''", code, re.DOTALL))
        if remove_quote:
            kernels = [kernel[3:-3] for kernel in kernels]
    return result, kernels

