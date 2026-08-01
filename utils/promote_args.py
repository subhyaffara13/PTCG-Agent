
def promote_args(new_args):
    def promote_arg(arg, promote_type):
        if (
            isinstance(arg, CppCSEVariable)
            and arg.dtype
            and promote_type
            and arg.dtype != promote_type
        ):
            arg = ops.to_dtype(arg, promote_type)
            arg = arg.value if isinstance(arg, OpsValue) else arg
            arg.dtype = promote_type
        return arg

    promote_type = get_promote_dtype(new_args)
    promote_fn = functools.partial(
        promote_arg,
        promote_type=promote_type,
    )
    if (
        all(
            new_arg.dtype is not None
            for new_arg in new_args
            if isinstance(new_arg, CppCSEVariable)
        )
        and promote_type
    ):
        new_args = list(map(promote_fn, new_args))
    return new_args


def promote_args(fun_name: str, *args: ArrayLike) -> list[Array]:
  """Convenience function to apply Numpy argument shape and dtype promotion."""
  check_arraylike(fun_name, *args)
  args = tuple(_check_jax_array_protocol(arg) for arg in args)
  _check_no_float0s(fun_name, *args)
  check_for_prngkeys(fun_name, *args)
  return promote_shapes(fun_name, *promote_dtypes(*args))

