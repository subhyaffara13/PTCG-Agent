
def uneven_size_corrected(p2c_att, query_layer: torch.Tensor, key_layer: torch.Tensor, relative_pos):
    if query_layer.size(-2) != key_layer.size(-2):
        pos_index = relative_pos[:, :, :, 0].unsqueeze(-1)
        return torch.gather(p2c_att, dim=2, index=pos_dynamic_expand(pos_index, p2c_att, key_layer))
    else:
        return p2c_att

