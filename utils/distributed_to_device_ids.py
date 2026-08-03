from typing import List

def distributed_to_device_ids() -> List[List[int]]:
  if not is_distributed_to_device_ids_initialized():
    raise ValueError('Please call initialize_distributed_to_device_ids().')
  return _DISTRIBUTED_TO_DEVICE_IDS

