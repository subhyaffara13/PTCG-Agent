
def _get_seq_length(self, layer_idx: int = 0) -> int:
    return self.layers[self.first_attention_layer].get_seq_length()

