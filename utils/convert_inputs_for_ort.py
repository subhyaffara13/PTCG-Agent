
def convert_inputs_for_ort(
    pt_inputs: dict,
    use_buffer_share: bool = False,
    past_seq_len: int = 0,
    max_seq_len: int = 2048,
):
    ort_inputs = {}
    for k, v in pt_inputs.items():
        if isinstance(v, np.ndarray):
            ort_inputs[k] = v
        elif k == "past_key_values":
            ort_inputs.update(flatten_past_kv_inputs(v))
        else:
            ort_inputs[k] = v.detach().cpu().numpy()

    # Reshape KV caches if using past-present-share-buffer
    if use_buffer_share:
        ort_inputs = enable_past_present_share_buffer(ort_inputs, past_seq_len, max_seq_len)

    return ort_inputs


def convert_inputs_for_ort(
    inputs: dict,
    model: InferenceSession,
):
    self_attn_kv_caches, cross_attn_kv_caches = None, None
    batch_size, num_heads, past_seq_len, head_size = 0, 0, 0, 0
    num_beams, max_seq_len = 1, 448
    if "past_key_values" in inputs:
        (self_attn_kv_caches, cross_attn_kv_caches) = group_past_key_values(inputs["past_key_values"])
        batch_size, num_heads, past_seq_len, head_size = self_attn_kv_caches[0].shape

    ort_inputs = {}
    model_inputs = list(map(lambda i: i.name, model.get_inputs()))  # noqa: C417
    use_buffer_sharing = "cache_indirection" in model_inputs
    for name in model_inputs:
        if name in {"audio_features", "encoder_input_ids"}:
            # Encoder input
            ort_inputs[name] = inputs["audio_features"].detach().cpu().numpy()
        elif name == "encoder_hidden_states":
            # Encoder output
            ort_inputs[name] = inputs["encoder_hidden_states"].detach().cpu().numpy()
        elif name in {"decoder_input_ids", "input_ids"}:
            # Decoder input
            ort_inputs[name] = inputs["decoder_input_ids"].detach().cpu().numpy()
        elif "past_key_self" in name or "past_value_self" in name:
            # Decoder input
            orig_kv_cache = self_attn_kv_caches.pop(0).detach().cpu().numpy()
            if use_buffer_sharing:
                new_kv_cache = np.zeros((batch_size, num_heads, max_seq_len, head_size), dtype=orig_kv_cache.dtype)
                new_kv_cache[:batch_size, :num_heads, :past_seq_len, :head_size] = orig_kv_cache
                ort_inputs[name] = new_kv_cache
            else:
                ort_inputs[name] = orig_kv_cache
        elif "past_key_cross" in name or "past_value_cross" in name:
            # Decoder input
            orig_kv_cache = cross_attn_kv_caches.pop(0).detach().cpu().numpy()
            ort_inputs[name] = orig_kv_cache
        elif name == "past_sequence_length":
            # Decoder input
            ort_inputs[name] = np.array([past_seq_len], dtype=np.int32)
        elif name == "cache_indirection":
            # Decoder input
            ort_inputs[name] = np.zeros((batch_size, num_beams, max_seq_len), dtype=np.int32)
        elif name == "alignment_heads":
            # Jump times input
            ort_inputs[name] = inputs["alignment_heads"].detach().cpu().numpy()
        elif name == "sot_sequence_length":
            # Jump times input
            ort_inputs[name] = inputs["sot_sequence_length"].detach().cpu().numpy()
        elif name == "segment_length":
            # Jump times input
            ort_inputs[name] = inputs["segment_length"].detach().cpu().numpy()
        elif "cross_qk" in name:
            # Jump times input
            ort_inputs[name] = inputs["QKs"].pop(0).detach().cpu().numpy()
        else:
            raise ValueError(f"Unknown name not recognized: {name}")

    return ort_inputs

