
def register_better_reload_error() -> None:
  ip = IPython.get_ipython()

  if ip is None:  # In tests
    return

  # What if this conflict with other `ip.set_custom_exc` ?
  # Ideally, should support multiple handlers
  ip.set_custom_exc((NameError,), _maybe_better_error)

