import functools

def set_up_omegaconf() -> None:
  """Registers handlers for OmegaConf types."""
  if omegaconf is None:
    raise RuntimeError(
        "Cannot set up OmegaConf support in treescope: omegaconf cannot be"
        " imported."
    )
  type_registries.TREESCOPE_HANDLER_REGISTRY[omegaconf.DictConfig] = (
      functools.partial(repr_lib.handle_custom_mapping, roundtrippable=True)
  )
  type_registries.TREESCOPE_HANDLER_REGISTRY[omegaconf.ListConfig] = (
      functools.partial(repr_lib.handle_custom_listlike, roundtrippable=True)
  )
  # Register canonical aliases for all types and functions omegaconf exports
  # in omegaconf.__all__.
  canonical_aliases.populate_from_public_api(
      omegaconf, canonical_aliases.prefix_filter("omegaconf")
  )

