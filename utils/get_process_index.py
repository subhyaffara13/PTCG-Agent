
def get_process_index() -> int:
  """Returns process index from torch if available, else from multihost."""
  try:
    import torch.distributed as dist  # pylint: disable=g-import-not-at-top

    if dist.is_initialized():
      return dist.get_rank()
  except ImportError:
    pass
  return multihost.process_index()

