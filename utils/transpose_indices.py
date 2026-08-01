
def transpose_indices(indices, dim_1_block, dim_2_block):
    return ((indices % dim_2_block) * dim_1_block + torch.div(indices, dim_2_block, rounding_mode="floor")).long()

