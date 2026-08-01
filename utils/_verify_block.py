
def _verify_block(block_name, dim_name, block, dim, should_divide=True):
  if block > dim:
    raise ValueError(
        f"{block_name}={block} should be smaller or equal to {dim_name}={dim}"
    )
  if should_divide and dim % block != 0:
    raise ValueError(
        f"{dim_name}={dim} should be divisible by {block_name}={block}"
    )

