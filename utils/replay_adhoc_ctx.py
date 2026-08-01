
def replay_adhoc_ctx(**adhoc_kwargs: Any):
  """Replay the adhoc context."""

  scope = adhoc_kwargs.pop('__scope__')

  match scope:
    case Scope.COLAB:
      from etils import ecolab  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

      return ecolab.adhoc(**adhoc_kwargs)
    case Scope.BINARY:
      # Added by LazyModule but not supported by binary_adhoc
      adhoc_kwargs.pop('collapse_prefix')

      from etils.epy.adhoc_utils import binary_import  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

      return binary_import.binary_adhoc(**adhoc_kwargs)
    case _:
      raise ValueError(f'Unknown scope: {scope}')

