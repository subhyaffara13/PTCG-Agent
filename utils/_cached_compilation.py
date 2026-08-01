
def _cached_compilation(computation, name,
                        tuple_args, allow_prop_to_inputs,
                        allow_prop_to_outputs, host_callbacks, backend,
                        da, compiler_options_kvs, pgle_profiler):
  # One would normally just write: dev = np.array(device_assignment)
  # The formulation below is substantially faster if there are many devices.
  dev = np.vectorize(lambda i: da[i], otypes=[object])(np.arange(len(da)))
  compiler_options = dict(compiler_options_kvs)

  compile_options = create_compile_options(
      computation, tuple_args, allow_prop_to_inputs, allow_prop_to_outputs,
      backend, dev, compiler_options)

  with dispatch.log_elapsed_time(
      "Finished XLA compilation of {fun_name} in {elapsed_time:.9f} sec",
      fun_name=name, event=dispatch.BACKEND_COMPILE_EVENT):
    xla_executable = compiler.compile_or_get_cached(
        backend, computation, dev, compile_options, host_callbacks,
        da, pgle_profiler)
  return xla_executable

