
def _pjit_call_impl_python(
    *args,
    jaxpr: core.ClosedJaxpr,
    in_shardings, out_shardings, in_layouts, out_layouts,
    donated_invars, ctx_mesh, name, keep_unused, inline,
    compiler_options_kvs):
  util.test_event("jit_cpp_cache_miss")
  pgle_compile_options, pgle_profiler = {}, None
  if config.enable_pgle.value and config.pgle_profiling_runs.value > 0:
    compilation_target_key = jaxpr
    pgle_profiler = _pgle_profiler_dict.get(compilation_target_key)
    if pgle_profiler is None:
      pgle_profiler = profiler.PGLEProfiler(
          config.pgle_profiling_runs.value,
          config.pgle_aggregation_percentile.value)
      _pgle_profiler_dict[compilation_target_key] = pgle_profiler

    # The method below will return FDO profile when module was profiled
    # config.jax_pgle_profiling_runs amount of times, otherwise the result will
    # be None.
    fdo_profile = pgle_profiler.consume_fdo_profile()
    if fdo_profile is not None:
      pgle_compile_options['fdo_profile'] = fdo_profile

  compiler_options_kvs = compiler_options_kvs + tuple(pgle_compile_options.items())
  # Passing mutable PGLE profile here since it should be extracted by JAXPR to
  # initialize the fdo_profile compile option.
  arg_types = map(convert_to_metaty, args)
  computation = _resolve_and_lower(
      arg_types, jaxpr=jaxpr, in_shardings=in_shardings,
      out_shardings=out_shardings, in_layouts=in_layouts,
      out_layouts=out_layouts, donated_invars=donated_invars,
      ctx_mesh=ctx_mesh, name=name, keep_unused=keep_unused,
      inline=inline, lowering_platforms=None,
      lowering_parameters=mlir.LoweringParameters(),
      pgle_profiler=pgle_profiler,
      compiler_options_kvs=compiler_options_kvs,
  )
  compiled = computation.compile()
  sharded_const_args = compiled.shard_const_args(computation.const_args)

  if config.distributed_debug.value:
    # Defensively only perform fingerprint logic if debug logging is enabled
    fingerprint = None
    if hasattr(compiled.runtime_executable(), "fingerprint"):
      fingerprint = compiled.runtime_executable().fingerprint
    if fingerprint is not None:
      fingerprint = fingerprint.hex()
    distributed_debug_log(
        ("Running pjit'd function", name), ("in_shardings", in_shardings),
        ("out_shardings", out_shardings), ("in_layouts", in_layouts),
        ("out_layouts", out_layouts), ("abstract args", map(core.typeof, args)),
        ("fingerprint", fingerprint))
  return (compiled.unsafe_call(*sharded_const_args, *args),
          compiled, pgle_profiler, sharded_const_args)

