
def register_autovisualize_magic():
  """Registers the ``%%autovisualize`` magic.

  This makes it possible to use ``%%autovisualize`` at the top of a cell to
  enable automatic visualization for that cell's outputs.

  Raises:
    RuntimeError: If IPython is not available.
  """
  if IPython is None:
    raise RuntimeError(
        "Cannot use `register_autovisualize_magic` outside of IPython."
    )
  IPython.get_ipython().register_magics(AutovisualizerMagic)

