from typing import Optional

def variable_with_axes(
    collection: str,
    name: str,
    init_fn,
    *init_args,
    axes: tuple[str, ...] | None = None,
    module: Optional['nn.Module'] = None,
    fallback: RulesFallback = RulesFallback.AXIS_IS_UNSHARDED,
    **init_kwargs,
):
  """Declares and returns a variable with logical axes in the current Module.

  See :mod:`flax.linen.module.variable` for original docstring.

  Args:
    collection: The name of the variable collection.
    name: The variable name.
    init_fn: The function that will be called to compute the initial value
      of this variable. This function will only be called the first time
      this parameter is used in this module.
    *init_args: The positional arguments to pass to init_fn.
    axes: A tuple of axis names, must match the rank of the variable array.
    module: Use an explicit module instead of deriving the most recent from
      dynamic module context.
    fallback: How sharding should behave if there is no rule covering some axis.
    **init_kwargs: The key-word arguments to pass to init_fn.

  Returns:
    A flax `PartitionedVariable` object referencing the initialized variable
    array.

  Raises:
    TypeError: if axes specification is mal-formed.
    ValueError: if specified logical axes don't match parameter rank.
  """
  # get current module if not explicitly provided
  if module is None:
    module = nn.module._context.module_stack[-1]  # pylint: disable=protected-access
    assert module is not None
  module_var = _core_variable_with_axes(
      module.scope,
      collection,
      name,
      init_fn,
      *init_args,
      axes=axes,
      fallback=fallback,
      **init_kwargs,
  )
  if axes is not None:
    # record logical axis constraint for global axis metadata
    module.sow(
        f'{collection}_axes',
        f'{name}_axes',
        AxisMetadata(axes),  # type: ignore
        reduce_fn=_param_with_axes_sow_reduce_fn,
    )
  return module_var

