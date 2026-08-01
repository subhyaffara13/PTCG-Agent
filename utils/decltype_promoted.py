
def decltype_promoted(*args):
    assert not any(isinstance(arg, CppCSEVariable) and arg.is_vec for arg in args), (
        "Promotion of vector types is not supported"
    )

    if (dt := get_promote_dtype(args)) is not None:
        return DTYPE_TO_CPP[dt]
    else:
        return f"decltype({args[0]})"

