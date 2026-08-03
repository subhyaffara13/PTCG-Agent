from typing import Callable

def _export_internal(
    fun_jit: stages.Wrapped,
    *,
    platforms: Sequence[str] | None = None,
    disabled_checks: Sequence[DisabledSafetyCheck] = (),
    _device_assignment_for_internal_jax2tf_use_only=None,
    override_lowering_rules=None,
    ) -> Callable[..., Exported]:
  """Exports native serialization for a JAX function.

  Note: this function exists only for internal usage by jax2tf. Use
    :mod:`jax.export` instead.
    See https://docs.jax.dev/en/latest/export/export.html

  See docstring of ``export`` for more details.
  """
  if not isinstance(fun_jit, stages.Wrapped):
    raise ValueError(
        f"Function to be exported must be the result of `jit` but is: {fun_jit}")

  def do_export(*args_specs, **kwargs_specs) -> Exported:
    if platforms is not None:
      actual_lowering_platforms = tuple(platforms)
    else:
      actual_lowering_platforms = (default_export_platform(),)

    # TODO: move to `lower`
    check_symbolic_scope_errors(fun_jit, args_specs, kwargs_specs)

    traced = fun_jit.trace(*args_specs, **kwargs_specs)
    lowered = traced.lower(
        lowering_platforms=actual_lowering_platforms,
        _private_parameters=mlir.LoweringParameters(
            override_lowering_rules=override_lowering_rules,
            for_export=True,
            hoist_constants_as_args=False,
            export_ignore_forward_compatibility=config.export_ignore_forward_compatibility.value))
    return _export_lowered(
        lowered, traced.jaxpr, traced.fun_name,
        disabled_checks=disabled_checks,
        _device_assignment_for_internal_jax2tf_use_only=_device_assignment_for_internal_jax2tf_use_only)
  return do_export

