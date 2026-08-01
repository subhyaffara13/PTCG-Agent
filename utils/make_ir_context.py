
def make_ir_context() -> ir.Context:
  """Creates an MLIR context suitable for JAX IR."""
  context = JaxIrContext()
  context.append_dialect_registry(upstream_dialects)
  context.load_all_available_dialects()

  context.set_thread_pool(global_thread_pool)
  dialects.sdy.register_dialect(context)
  dialects.mpmd.register_dialect(context)
  dialects.mhlo.register_mhlo_dialect(context)
  dialects.chlo.register_dialect(context)
  dialects.hlo.register_dialect(context)
  # If built in debug mode, and MLIR is in a multithreaded context, enabling
  # multi threaded execution aborts the process if we try to register a new
  # dialect after this point. The dialect registry in a context is not thread
  # safe, and a fatal error is much better than a data race.
  # jax_mlir_ext.enter_multi_threaded_execution(context)
  # TODO(phawkins): clean up users who add their own dialects to JAX's contexts
  # and enable this.
  return context

