import logging

def _check_if_hanging_assertions():
  if _ai.CHEXIFY_STORAGE.wait_fns:
    logging.warning(
        '[Chex] Some of chexify assertion statuses were not inspected due to '
        'async exec (https://jax.readthedocs.io/en/latest/async_dispatch.html).'
        ' Consider calling `chex.block_until_chexify_assertions_complete()` at '
        'the end of computations that rely on jitted chex assertions.')
    block_until_chexify_assertions_complete()

