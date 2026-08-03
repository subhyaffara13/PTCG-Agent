from typing import Callable

def _slice_mask_info(
    *,
    block_mask: np.ndarray,
    data_next: np.ndarray,
    mask_next: np.ndarray | None,
    head_shards: int,
    slice_function: Callable[[np.ndarray], np.ndarray],
):
  new_block_mask = []
  new_data_next = []
  new_mask_next = []
  for head_shard in range(head_shards):
    head_block_mask = block_mask[head_shard]
    head_block_mask = slice_function(head_block_mask)
    new_block_mask.append(head_block_mask)

    head_data_next = data_next[head_shard]
    head_data_next = slice_function(head_data_next)
    new_data_next.append(head_data_next)

    if mask_next is not None:
      head_mask_next = mask_next[head_shard]
      head_mask_next = slice_function(head_mask_next)
      new_mask_next.append(head_mask_next)

  block_mask = np.stack(new_block_mask, axis=0)
  data_next = np.stack(new_data_next, axis=0)
  if mask_next is not None:
    mask_next = np.stack(new_mask_next, axis=0)

  return block_mask, data_next, mask_next

