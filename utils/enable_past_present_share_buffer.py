
def enable_past_present_share_buffer(ort_inputs: dict, past_seq_len: int, max_seq_len: int):
    for k, v in ort_inputs.items():
        # Allocate new buffers with max_sequence_length for GQA
        if "cache" in k or "past_key_values" in k:
            # Copy v (BxSxPxH) into new_v (BxSxMxH)
            batch_size, num_heads, _, head_size = v.shape
            new_v = np.zeros((batch_size, num_heads, max_seq_len, head_size), dtype=v.dtype)
            new_v[:batch_size, :num_heads, :past_seq_len, :head_size] = v
            ort_inputs[k] = new_v
    return ort_inputs

