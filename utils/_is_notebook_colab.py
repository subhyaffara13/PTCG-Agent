import sys

def _is_notebook_colab() -> bool:
  """Returns True if notebook is colab."""
  return 'google.colab' in sys.modules

