
def process_index() -> int:
  """Customized logic for obtaining JAX process index."""
  if use_experimental_distributed_process_id():
    logging.log_first_n(
        logging.INFO,
        '[thread=%s] Using distributed process id.',
        1,
        threading.current_thread().name,
    )
    return jax._src.distributed.global_state.process_id  # pylint: disable=protected-access
  else:
    return jax.process_index()


def process_index() -> int:
  if is_pathways_backend():
    return jax.process_index()
  # Note that jax.process_index() does not return the same thing as
  # global_state.process_id. We rely on the latter to work with barriers over a
  # subset of processes.
  return jax._src.distributed.global_state.process_id  # pylint: disable=protected-access


def process_index(
    backend: str | xla_client.Client | None = None
) -> int:
  """Returns the integer process index of this process.

  On most platforms, this will always be 0. This will vary on multi-process
  platforms though.

  Args:
    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the xla backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.

  Returns:
    Integer process index.
  """
  return get_backend(backend).process_index()

