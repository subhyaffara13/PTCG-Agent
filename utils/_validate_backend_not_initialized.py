
def _validate_backend_not_initialized(name, new_val):
  if backends_are_initialized():
    if getattr(config.config, name) == new_val:
      return
    raise RuntimeError(
        f"{name} config should be updated before backends are"
        " initialized i.e. before any JAX operation is executed. You should"
        " initialize this config immediately after `import jax`.")

