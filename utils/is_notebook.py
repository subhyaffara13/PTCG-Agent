import sys

def is_notebook() -> bool:
    """Return `True` if code is executed in a notebook (Jupyter, Colab, QTconsole).

    Taken from https://stackoverflow.com/a/39662359.
    Adapted to make it work with Google colab as well.
    """
    try:
        shell_class = get_ipython().__class__  # type: ignore # noqa: F821
        for parent_class in shell_class.__mro__:  # e.g. "is subclass of"
            if parent_class.__name__ == "ZMQInteractiveShell":
                return True  # Jupyter notebook, Google colab or qtconsole
        return False
    except NameError:
        return False  # Probably standard Python interpreter


def is_notebook() -> bool:
  """Returns True if running in a notebook (Colab, Jupyter) environment."""
  # Use sys.module as we do not want to trigger an import (slow)
  # Check whether we're running in a IPython notebook (and not terminal)
  if IPython := sys.modules.get('IPython'):  # pylint: disable=invalid-name
    ipython = IPython.get_ipython()
    if ipython and 'IPKernelApp' in ipython.config:
      return True
  return False

