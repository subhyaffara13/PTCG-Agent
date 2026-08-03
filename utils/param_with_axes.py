from typing import Optional

def param_with_axes(
    name: str,
    init_fn,
    *init_args,
    axes: tuple[str, ...] | None = None,
    module: Optional['nn.Module'] = None,
    **init_kwargs,
):
  """Declares and returns a parameter with logical axes in the current Module.

  See :mod:`flax.linen.module.param` for original docstring.

  Args:
    name: The parameter name.
    init_fn: The function that will be called to compute the initial value
      of this variable. This function will only be called the first time
      this parameter is used in this module.
    *init_args: The positional arguments to pass to init_fn.
    axes: A tuple of axis names, must match the rank of the param array.
    module: Use an explicit module instead of deriving the most recent from
      dynamic module context.
    **init_kwargs: The key-word arguments to pass to init_fn.

  Returns:
    The value of the initialized parameter.

  Raises:
    TypeError: if axes specification is mal-formed.
    ValueError: if specified logical axes don't match parameter rank.
  """
  # get current module if not explicitly provided
  if module is None:
    module = nn.module._context.module_stack[-1]  # pylint: disable=protected-access
    assert module is not None
  # define/fetch parameter on that module
  module_param = module.param(name, init_fn, *init_args, **init_kwargs)
  if axes is not None:
    # apply logical axis constraint immediately
    module_param = with_sharding_constraint(
        module_param, jax.sharding.PartitionSpec(*axes)
    )
    # record logical axis constraint for global axis metadata
    module.sow(
        'params_axes',
        f'{name}_axes',
        AxisMetadata(axes),  # type: ignore
        reduce_fn=_param_with_axes_sow_reduce_fn,
    )
  return module_param

