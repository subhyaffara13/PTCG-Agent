
def _patch_function(fn: FunctionType, nargs: int) -> FunctionType:
    co = fn.__code__
    co_flags = co.co_flags & ~HAS_VARSTUFF
    co_args: tuple[Any, ...]
    if hasattr(co, "co_qualname"):
        # Python-3.11+ code signature
        co_args = (
            nargs,
            0,
            0,
            co.co_nlocals,
            co.co_stacksize,
            co_flags,
            co.co_code,
            co.co_consts,
            co.co_names,
            co.co_varnames,
            co.co_filename,
            co.co_name,
            co.co_qualname,  # type: ignore[attr-defined]
            co.co_firstlineno,
            co.co_linetable,
            co.co_exceptiontable,  # type: ignore[attr-defined]
            co.co_freevars,
            co.co_cellvars,
        )
    elif hasattr(co, "co_posonlyargcount"):
        co_args = (
            nargs,
            0,
            0,
            co.co_nlocals,
            co.co_stacksize,
            co_flags,
            co.co_code,
            co.co_consts,
            co.co_names,
            co.co_varnames,
            co.co_filename,
            co.co_name,
            co.co_firstlineno,
            co.co_lnotab,
            co.co_freevars,
            co.co_cellvars,
        )
    else:
        co_args = (
            nargs,
            0,
            co.co_nlocals,
            co.co_stacksize,
            co_flags,
            co.co_code,
            co.co_consts,
            co.co_names,
            co.co_varnames,
            co.co_filename,
            co.co_name,
            co.co_firstlineno,
            co.co_lnotab,
            co.co_freevars,
            co.co_cellvars,
        )
    new_code = CodeType(*co_args)  # type: ignore[arg-type]
    return FunctionType(
        new_code, fn.__globals__, fn.__name__, fn.__defaults__, fn.__closure__
    )

