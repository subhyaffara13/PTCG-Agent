
def register_context_manager_magic():
  """Registers the ``%%with`` magic.

  This makes it possible to use ``%%with`` at the top of a cell to enable
  automatic visualization for that cell's outputs.

  Raises:
    RuntimeError: If IPython is not available.
  """
  if IPython is None:
    raise RuntimeError(
        "Cannot use `register_context_manager_magic` outside of IPython."
    )
  IPython.get_ipython().register_magics(ContextManagerMagic)

