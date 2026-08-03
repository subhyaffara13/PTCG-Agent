from typing import Callable

def prepare_function_arguments(
    func: Callable, args: tuple, kwargs: dict, *, num_required_args: int
) -> tuple[tuple, dict]:
    """
    Prepare arguments for jitted function. As numba functions do not support kwargs,
    we try to move kwargs into args if possible.

    Parameters
    ----------
    func : function
        User defined function
    args : tuple
        User input positional arguments
    kwargs : dict
        User input keyword arguments
    num_required_args : int
        The number of leading positional arguments we will pass to udf.
        These are not supplied by the user.
        e.g. for groupby we require "values", "index" as the first two arguments:
        `numba_func(group, group_index, *args)`, in this case num_required_args=2.
        See :func:`pandas.core.groupby.numba_.generate_numba_agg_func`

    Returns
    -------
    tuple[tuple, dict]
        args, kwargs

    """
    if not kwargs:
        return args, kwargs

    # the udf should have this pattern: def udf(arg1, arg2, ..., *args, **kwargs):...
    signature = inspect.signature(func)
    arguments = signature.bind(*[_sentinel] * num_required_args, *args, **kwargs)
    arguments.apply_defaults()
    # Ref: https://peps.python.org/pep-0362/
    # Arguments which could be passed as part of either *args or **kwargs
    # will be included only in the BoundArguments.args attribute.
    args = arguments.args
    kwargs = arguments.kwargs

    if kwargs:
        # Note: in case numba supports keyword-only arguments in
        # a future version, we should remove this check. But this
        # seems unlikely to happen soon.

        raise NumbaUtilError(
            "numba does not support keyword-only arguments"
            "https://github.com/numba/numba/issues/2916, "
            "https://github.com/numba/numba/issues/6846"
        )

    args = args[num_required_args:]
    return args, kwargs

