
def below_or_on_diag(r, r_blk_size, c, c_blk_size):
  # A block is considered below or on diagonal as long as the bottom left
  # corner of the block is below or on diagonal.
  return ((r + 1) * r_blk_size - 1) > (c * c_blk_size)

