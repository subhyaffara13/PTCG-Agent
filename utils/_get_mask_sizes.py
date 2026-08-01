
def _get_mask_sizes(self, query_length: int, layer_idx: int) -> tuple[int, int]:
    return self.layers[self.first_attention_layer].get_mask_sizes(query_length)

