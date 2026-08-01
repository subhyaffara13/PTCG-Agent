
def compute_attention_span(query_layer: torch.Tensor, key_layer: torch.Tensor, max_relative_positions: int):
    return torch.tensor(min(max(query_layer.size(-2), key_layer.size(-2)), max_relative_positions))

