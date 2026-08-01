
def check_dtype(f_name, t, dtype, *additional_dtypes):
    check(
        t.dtype == dtype
        and t.dtype
        in ((torch.half, torch.bfloat16, torch.float) + tuple(*additional_dtypes)),
        f"{f_name}(): all inputs are expected to be of the same dtype "
        f"and one of (half, bfloat16, float32) or {additional_dtypes}, "
        f"but got dtype == {t.dtype}.",
    )


def check_dtype(
    buffer: IndentedBuffer, var: CSEVariableType, dtype: torch.dtype
) -> None:
    backend = get_current_backend()
    if config.test_configs.runtime_triton_dtype_assert and backend == "triton":
        buffer.writeline(f"tl.static_assert({var}.dtype == {triton_type(dtype)})")
    elif config.test_configs.static_cpp_dtype_assert and backend == "cpp":
        from .cpp_utils import CppCSEVariable, DTYPE_TO_CPP

        assert isinstance(var, CppCSEVariable), type(var)
        if dtype == torch.bool:
            if var.is_vec:
                is_same_dt = f"IsVecMaskType<decltype({var})>::value"
            else:
                # operator&(bool, bool) returns int and it can be used as boolean in C++
                is_same_dt = f"std::is_same_v<decltype({var}), bool> || std::is_same_v<decltype({var}), int>"
        else:
            c_var_type = f"decltype({var})"
            if var.is_vec:
                c_var_type = f"typename {c_var_type}::value_type"
            is_same_dt = f"std::is_same_v<{c_var_type}, {DTYPE_TO_CPP[dtype]}>"

        buffer.writeline(f"static_assert({is_same_dt});")


def check_dtype(a: Tensor, b: Tensor) -> bool:
    return a.is_floating_point() and b.is_floating_point()


def check_dtype(request):
    """
    Fixture returning `True` or `False`, determining whether to check
    if the `dtype` is identical or not, when comparing two data structures,
    e.g. `Series`, `SparseArray` or `DataFrame`.
    """
    return request.param

