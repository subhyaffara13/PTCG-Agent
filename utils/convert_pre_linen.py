from typing import Any

def convert_pre_linen(params: PyTree) -> PyTree:
  """Converts a pre-Linen parameter pytree.

  In pre-Linen API submodules were numbered incrementally, independent of the
  submodule class. With Linen this behavior has changed to keep separate
  submodule counts per module class.

  Consider the following module::

    class Model(nn.Module):
      @nn.compact
      def __call__(self, x):
        x = nn.Conv(1, 1)(x)
        x = nn.Dense(1)(x)
        return x

  In pre-Linen the resulting params would have had the structure:

    ``{'Conv_0': { ... }, 'Dense_1': { ... } }``

  With Linen the resulting params would instead have had the structure:

    ``{'Conv_0': { ... }, 'Dense_0': { ... } }``

  To convert from pre-Linen format to Linen simply call::

    params = convert_pre_linen(pre_linen_params)

  Note that you can also use this utility to convert pre-Linen collections
  because they're following the same module naming. Note though that collections
  were "flat" in pre-Linen and first need to be unflattened before they can be
  used with this function::

    batch_stats = convert_pre_linen(flax.traverse_util.unflatten_dict({
        tuple(k.split('/')[1:]): v
        for k, v in pre_linen_model_state.as_dict().items()
    }))

  Then Linen variables can be defined from these converted collections::

    variables = {'params': params, 'batch_stats': batch_stats}

  Args:
    params: Parameter pytree in pre-Linen format. If the pytree is already in
      Linen format, then the returned pytree is unchanged (i.e. this function
      can safely be called on any loaded checkpoint for use with Linen).

  Returns:
    Parameter pytree with Linen submodule naming.
  """
  if not isinstance(params, (dict, core.FrozenDict)):
    return params
  params_renamed = {}
  counts: dict[Any, Any] = {}
  names = natural_sort(params.keys())
  for name in names:
    value = params[name]
    match = MODULE_NUM_RE.match(name)
    if match:
      module = match.group(1)
      num = counts.get(module, 0)
      name = f'{module}_{num}'
      counts[module] = num + 1
    params_renamed[name] = convert_pre_linen(value)

  if isinstance(params, core.FrozenDict):
    params_renamed = core.freeze(params_renamed)  # type: ignore
  return params_renamed

