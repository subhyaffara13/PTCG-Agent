
def _thread_map_callback(jaxpr, token, device_id, num_threads, consts, invals,
                         *, on_exception):
  # TODO(jburnim): Convert all JAX values in `consts` and `invals` to NumPy
  # values before passing them to a different thread.
  device_id = int(device_id) if device_id is not None else None
  consts = jax.tree.map(np.array, consts)
  invals = jax.tree.map(np.array, invals)
  num_threads = int(num_threads)
  threads = []
  with futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    for i in range(num_threads):
      # `jaxpr` is the traced representation of a function whose first argument
      # is the thread ID. Hence,
      #   - prepend the thread ID onto the `invals`; and
      #   - flatten the arguments that are to be passed through to the
      #     evaluation of `jaxpr`.
      args = (jnp.int32(i), *invals)
      flat_args, _ = jax.tree.flatten(args)
      threads.append(executor.submit(_run_jaxpr, jaxpr, consts, *flat_args))
    exceptions = []
    for i in range(num_threads):
      try:
        threads[i].result()
      except Exception as e:
        exceptions.append(e)
  if exceptions:
    on_exception(exceptions[0], device_id=device_id)
    # TODO(jburnim): Improve exception propagation here.  That is:
    #  - exceptions[0] might be an uninformative exception that just reports
    #    that the computation failed on a different device/core.
    #  - The cause of the exception (which may includes the actual line number
    #    in the user's kernel) is stripped by the XLA runtime.  (Maybe we could
    #    stash the exception in a global in Python somewhere.)
    raise exceptions[0]
  return token

