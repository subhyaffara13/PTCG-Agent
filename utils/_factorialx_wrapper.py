
def _factorialx_wrapper(fname, n, k, exact, extend):
    """
    Shared implementation for factorial, factorial2 & factorialk.
    """
    if extend not in ("zero", "complex"):
        raise ValueError(
            f"argument `extend` must be either 'zero' or 'complex', received: {extend}"
        )
    if exact and extend == "complex":
        raise ValueError("Incompatible options: `exact=True` and `extend='complex'`")

    msg_unsup = (
        "Unsupported data type for {vname} in {fname}: {dtype}\n"
    )
    if fname == "factorial":
        msg_unsup += (
            "Permitted data types are integers and floating point numbers, "
            "as well as complex numbers if `extend='complex' is passed."
        )
    else:
        msg_unsup += (
            "Permitted data types are integers, as well as floating point "
            "numbers and complex numbers if `extend='complex' is passed."
        )
    msg_exact_not_possible = (
        "`exact=True` only supports integers, cannot use data type {dtype}"
    )
    msg_needs_complex = (
        "In order to use non-integer arguments, you must opt into this by passing "
        "`extend='complex'`. Note that this changes the result for all negative "
        "arguments (which by default return 0)."
    )

    if fname == "factorial2":
        msg_needs_complex += (" Additionally, it will rescale the values of the double"
                              " factorial at even integers by a factor of sqrt(2/pi).")
    elif fname == "factorialk":
        msg_needs_complex += (" Additionally, it will perturb the values of the"
                              " multifactorial at most positive integers `n`.")
        # check type of k
        if not _is_subdtype(type(k), ["i", "f", "c"]):
            raise ValueError(msg_unsup.format(vname="`k`", fname=fname, dtype=type(k)))
        elif _is_subdtype(type(k), ["f", "c"]) and extend != "complex":
            raise ValueError(msg_needs_complex)
        # check value of k
        if extend == "zero" and k < 1:
            msg = f"For `extend='zero'`, k must be a positive integer, received: {k}"
            raise ValueError(msg)
        elif k == 0:
            raise ValueError("Parameter k cannot be zero!")

    # factorial allows floats also for extend="zero"
    types_requiring_complex = "c" if fname == "factorial" else ["f", "c"]

    # don't use isscalar due to numpy/numpy#23574; 0-dim arrays treated below
    if np.ndim(n) == 0 and not isinstance(n, np.ndarray):
        # scalar cases
        if not _is_subdtype(type(n), ["i", "f", "c", type(None)]):
            raise ValueError(msg_unsup.format(vname="`n`", fname=fname, dtype=type(n)))
        elif _is_subdtype(type(n), types_requiring_complex) and extend != "complex":
            raise ValueError(msg_needs_complex)
        elif n is None or np.isnan(n):
            complexify = (extend == "complex") and _is_subdtype(type(n), "c")
            return np.complex128("nan+nanj") if complexify else np.float64("nan")
        elif extend == "zero" and n < 0:
            return 0 if exact else np.float64(0)
        elif n in {0, 1}:
            return 1 if exact else np.float64(1)
        elif exact and _is_subdtype(type(n), "i"):
            # calculate with integers; cast away other int types (like unsigned)
            return _range_prod(1, int(n), k=k)
        elif exact:
            # only relevant for factorial
            raise ValueError(msg_exact_not_possible.format(dtype=type(n)))
        # approximation
        return _factorialx_approx_core(n, k=k, extend=extend)

    # arrays & array-likes
    n = asarray(n)

    if not _is_subdtype(n.dtype, ["i", "f", "c"]):
        raise ValueError(msg_unsup.format(vname="`n`", fname=fname, dtype=n.dtype))
    elif _is_subdtype(n.dtype, types_requiring_complex) and extend != "complex":
        raise ValueError(msg_needs_complex)
    elif exact and _is_subdtype(n.dtype, ["f"]):
        # only relevant for factorial
        raise ValueError(msg_exact_not_possible.format(dtype=n.dtype))

    if n.size == 0:
        # return empty arrays unchanged
        return n
    elif exact:
        # calculate with integers
        return _factorialx_array_exact(n, k=k)
    # approximation
    return _factorialx_array_approx(n, k=k, extend=extend)

