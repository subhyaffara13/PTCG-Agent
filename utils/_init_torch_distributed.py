import logging
import os

def _init_torch_distributed() -> None:
  """Initializes Torch distributed system."""
  if not dist.is_initialized():

    # External OSS Initialization (Vanilla PyTorch)
    logging.info(
        'torch.distributed not initialized, attempting vanilla init...')
    if 'TEST_TMPDIR' not in os.environ and 'MASTER_ADDR' not in os.environ:
      # Single-process fallback (e.g., local testing)
      logging.info('Setting local fallback env vars...')
      os.environ.setdefault('MASTER_ADDR', 'localhost')
      os.environ.setdefault('MASTER_PORT', '12355')
      dist.init_process_group(backend='nccl', rank=0, world_size=1)
    else:
      # Torchrun / Distributed launch
      try:
        dist.init_process_group(backend='cpu:gloo,cuda:nccl')
        logging.info(
            "Initialized torch.distributed with backend 'cpu:gloo,cuda:nccl',"
            ' rank %d, world size %d',
            dist.get_rank(),
            dist.get_world_size(),
        )
      except Exception as e:
        logging.exception(
            'Failed to initialize torch.distributed via dist: %s', e
        )
        raise

