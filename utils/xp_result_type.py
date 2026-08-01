
def xp_result_type(*args, force_floating=False, xp):
    """
    Returns the dtype that results from applying type promotion rules
    (see Array API Standard Type Promotion Rules) to the arguments. Augments
    standard `result_type` in a few ways:

    - There is a `force_floating` argument that ensures that the result type
      is floating point, even when all args are integer.
    - When a TypeError is raised (e.g. due to an unsupported promotion)
      and `force_floating=True`, we define a custom rule: use the result type
      of the default float and any other floats passed. See
      https://github.com/scipy/scipy/pull/22695/files#r1997905891
      for rationale.
    - This function accepts array-like iterables, which are immediately converted
      to the namespace's arrays before result type calculation. Consequently, the
      result dtype may be different when an argument is `1.` vs `[1.]`.

    Typically, this function will be called shortly after `array_namespace`
    on a subset of the arguments passed to `array_namespace`.
    """
    # prevent double conversion of iterable to array
    # avoid `np.iterable` for torch arrays due to pytorch/pytorch#143334
    # don't use `array_api_compat.is_array_api_obj` as it returns True for NumPy scalars
    args = [(_asarray(arg, subok=True, xp=xp) if is_torch_array(arg) or np.iterable(arg)
            else arg) for arg in args]
    args_not_none = [arg for arg in args if arg is not None]
    if force_floating:
        args_not_none.append(1.0)

    try:  # follow library's preferred promotion rules
        return xp.result_type(*args_not_none)
    except TypeError:  # mixed type promotion isn't defined
        if not force_floating:
            raise
        # use `result_type` of default floating point type and any floats present
        # This can be revisited, but right now, the only backends that get here
        # are array-api-strict (which is not for production use) and PyTorch
        # (due to data-apis/array-api-compat#279).
        float_args = []
        for arg in args_not_none:
            arg_array = xp.asarray(arg) if np.isscalar(arg) else arg
            dtype = getattr(arg_array, 'dtype', arg)
            if xp.isdtype(dtype, ('real floating', 'complex floating')):
                float_args.append(arg)
        return xp.result_type(*float_args, xp_default_dtype(xp))

