
def _ipython_supports_tracebackhide() -> bool:
  """Returns true if the IPython version supports __tracebackhide__."""
  import IPython  # pyrefly: ignore[missing-import]
  return IPython.version_info[:2] >= (7, 17)

