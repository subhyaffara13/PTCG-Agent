from typing import Any, Callable

def _make_async_execution_fun(
    info: FunctionInfo,
    specialization: Specialization,
) -> Callable[..., Any]:
  """Makes a function that asynchronously executes the function."""
  assert specialization.in_specs_treedef is not None
  assert specialization.in_specs_leaves is not None
  assert specialization.out_specs_treedef is not None
  assert specialization.out_specs_leaves is not None
  assert specialization.devices is not None

  name = getattr(info.fun, "__name__", "unknown")
  return _compile_to_executable(
      name=name,
      fun=info.fun,
      in_specs_treedef=specialization.in_specs_treedef,
      in_specs_leaves=specialization.in_specs_leaves,
      out_specs_treedef=specialization.out_specs_treedef,
      out_specs_leaves=specialization.out_specs_leaves,
      devices=specialization.devices,
  )

