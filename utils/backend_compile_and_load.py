from typing import Any

def backend_compile_and_load(
    backend: xc.Client,
    module: ir.Module,
    executable_devices: xc.DeviceList,
    options: xc.CompileOptions,
    host_callbacks: Sequence[Any],
) -> xc.LoadedExecutable:
  sym_name = module.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value

  if (options.executable_build_options.fdo_profile is not None
      and len(options.executable_build_options.fdo_profile)):
    logger.debug(
        "Compiling module %s with FDO profile of length %d",
        module_name,
        len(options.executable_build_options.fdo_profile),
    )

  try:
    # we use a separate function call to ensure that XLA compilation appears
    # separately in Python profiling results
    # TODO(dsuo): Simplify this logic once we delete _jax.CompileOnlyPyClient.
    if isinstance(backend, _jax.CompileOnlyPyClient):
      # When a real backend is available for the same platform, use it for
      # cross-compilation. The real client provides hardware access (e.g.,
      # for GPU kernel autotuning) while the topology specifies the target.
      cross_compile_backend = _get_cross_compile_backend(backend)
      if cross_compile_backend is not None and not host_callbacks:
        cross_compile_topology = xc.get_topology_for_devices(backend.devices())
        return cross_compile_backend.compile(
            module,
            topology=cross_compile_topology,
            compile_options=options,
        )
      if host_callbacks:
        return backend.compile(  # pyrefly: ignore[bad-return]
            module,
            executable_devices=executable_devices,
            compile_options=options,
            host_callbacks=host_callbacks,
        )
      # Some backends don't have `host_callbacks` option yet
      # TODO(sharadmv): remove this fallback when all backends allow `compile`
      # to take in `host_callbacks`
      return backend.compile(  # pyrefly: ignore[bad-return]
          module,
          executable_devices=executable_devices,
          compile_options=options,
      )
    else:
      if host_callbacks:
        return backend.compile_and_load(
            module,
            executable_devices=executable_devices,
            compile_options=options,
            host_callbacks=host_callbacks,
        )
      # Some backends don't have `host_callbacks` option yet
      # TODO(sharadmv): remove this fallback when all backends allow `compile`
      # to take in `host_callbacks`
      return backend.compile_and_load(
          module,
          executable_devices=executable_devices,
          compile_options=options,
      )
  except _jax.JaxRuntimeError as e:
    for error_handler in _XLA_RUNTIME_ERROR_HANDLERS:
      handler_result = error_handler(e)
      if handler_result is not None:
        raise handler_result from e
    raise e

