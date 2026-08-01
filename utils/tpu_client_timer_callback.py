
def tpu_client_timer_callback(timer_secs: float) -> xla_client.Client | None:
  def _log_warning():
    warnings.warn(
      f'TPU backend initialization is taking more than {timer_secs} seconds. '
      'Did you run your code on all TPU hosts? '
      'See https://docs.jax.dev/en/latest/multi_process.html '
      'for more information.')

  # Will log a warning after `timer_secs`.
  t = threading.Timer(timer_secs, _log_warning)
  t.start()

  try:
    client = make_tpu_client(
        get_tpu_library_path(),
        _options_from_jax_configs("tpu"))
  finally:
    t.cancel()

  return client

