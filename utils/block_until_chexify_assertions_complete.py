
def block_until_chexify_assertions_complete() -> None:
  """Waits until all asynchronous checks complete.

  See `chexify` for more detail.
  """
  for wait_fn in _ai.CHEXIFY_STORAGE.wait_fns:
    wait_fn()

