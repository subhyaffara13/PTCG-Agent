
def get_axial_mask(mask):
    """
    Helper to convert B x L mask of valid positions to axial mask used in row column attentions.

    Input:
      mask: B x L tensor of booleans

    Output:
      mask: B x L x L tensor of booleans
    """

    if mask is None:
        return None

    if len(mask.shape) != 2:
        raise ValueError(f"`mask` should be a 2d-tensor, got {len(mask.shape)} dims.")
    batch_dim, seq_dim = mask.shape
    m = mask.unsqueeze(1).expand(batch_dim, seq_dim, seq_dim)
    m = m.reshape(batch_dim * seq_dim, seq_dim)
    return m

