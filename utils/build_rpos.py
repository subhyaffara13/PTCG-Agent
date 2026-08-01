
def build_rpos(query_layer: torch.Tensor, key_layer: torch.Tensor, relative_pos):
    if query_layer.size(-2) != key_layer.size(-2):
        return build_relative_position(query_layer, key_layer)
    else:
        return relative_pos


def build_rpos(query_layer, key_layer, relative_pos, position_buckets: int, max_relative_positions: int):
    if key_layer.size(-2) != query_layer.size(-2):
        return build_relative_position(
            key_layer,
            key_layer,
            bucket_size=position_buckets,
            max_position=max_relative_positions,
        )
    else:
        return relative_pos

