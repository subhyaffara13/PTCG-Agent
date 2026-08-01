
def _call_threadmap_callback(token, device_id, jaxpr, num_threads, consts,
                             invals, use_ordered_callback, on_exception):
  # NOTE: At runtime, _thread_map_callback will lower and compile the
  # given jaxpr.  (JAX's caches should ensure the jaxpr is only lowered and
  # compiled once.)
  #
  # TODO(jburnim): Would it be worth trying to lower/compile the jaxpr at
  # lowering/compilation time?  E.g., by using a custom primitive here, could
  # we lower/compile jaxpr at lowering time, and then pass the compiled
  # function to the callback?
  return callback.io_callback(
      functools.partial(_thread_map_callback, jaxpr, on_exception=on_exception),
      jax.ShapeDtypeStruct((), jnp.int32),
      token,
      device_id,
      num_threads,
      consts,
      invals,
      ordered=use_ordered_callback,
  )

