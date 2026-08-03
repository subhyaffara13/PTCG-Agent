from typing import Callable

def _get_module_table(
  module: module_lib.Module,
  depth: int | None,
  show_repeated: bool,
  compute_flops: bool,
  compute_vjp_flops: bool,
) -> Callable[..., Table]:
  """A function that takes a Module and returns function with the same signature
  as `init` but returns the Table representation of the Module."""

  def _get_table_fn(*args, **kwargs):
    with module_lib._tabulate_context():

      def _get_variables():
        return module.init(*args, **kwargs)
      # TODO(cgarciae): is it possible to avoid leaking tracers for summaries?
      with jax.check_tracer_leaks(False):
        variables = jax.eval_shape(_get_variables)
      calls = module_lib._context.call_info_stack[-1].calls
      calls.sort(key=lambda c: c.index)

    collections: set[str] = set(variables.keys())
    rows = []
    all_paths: set[tuple[str, ...]] = {call.path for call in calls}
    visited_paths: set[tuple[str, ...]] = set()

    for c in calls:
      call_depth = len(c.path)
      inputs = _process_inputs(c.args, c.kwargs)

      if c.path in visited_paths or not hasattr(c.module, c.method):
        if not show_repeated:
          continue
        module_vars = {}
        counted_vars = {}
      elif depth is not None:
        if call_depth > depth:
          continue
        module_vars, _ = _get_module_variables(c.path, variables, all_paths)
        if call_depth == depth:
          counted_vars = _get_path_variables(c.path, variables)
        else:
          counted_vars = module_vars
      else:
        module_vars, _ = _get_module_variables(c.path, variables, all_paths)
        counted_vars = module_vars

      visited_paths.add(c.path)
      rows.append(
        Row(
          c.path,
          c.module.copy(parent=None),
          c.method,
          inputs,
          c.outputs,
          module_vars,
          counted_vars,
          *_get_call_flops(c, compute_flops, compute_vjp_flops),
        )
      )

    return Table(module, tuple(collections), rows)

  return _get_table_fn

