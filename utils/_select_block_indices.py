
def _select_block_indices(i):
  def block_transform(*block_indices):
    return block_indices[i]
  return block_transform

