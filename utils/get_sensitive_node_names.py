import re

def get_sensitive_node_names(matmul_nodes: list[str], encoder_layers: int, decoder_layers: int):
    """Identify sensitive MatMul nodes that should use INT8 in k_quant_mixed.

    Follows the llama.cpp k-quant mixed strategy adapted for Whisper encoder-decoder:
      - First/last ~12.5% of layers + every 3rd layer in between are "sensitive layers"
      - Within sensitive layers: attention Q/K/V projections and FFN fc2 (down projection) get INT8
      - proj_out (LM head) always gets INT8

    Reference: llama.cpp/src/llama-quant.cpp#L136

    Args:
        matmul_nodes: list of MatMul node names from the ONNX graph.
        encoder_layers: number of encoder layers in the model.
        decoder_layers: number of decoder layers in the model.

    Returns:
        list of node names that should be quantized to INT8.
    """

    def get_sensitive_layer_indices(num_layers):
        return [
            i
            for i in range(num_layers)
            if i < num_layers / 8 or i >= 7 * num_layers / 8 or (i - round(num_layers / 8)) % 3 == 2
        ]

    enc_sensitive_layers = set(get_sensitive_layer_indices(encoder_layers))
    dec_sensitive_layers = set(get_sensitive_layer_indices(decoder_layers))

    # Patterns for sensitive MatMul types within a sensitive layer:
    # - Attention projections: q_proj, k_proj, v_proj (most sensitive to quantization)
    # - FFN fc2 / out_proj equivalent (the down projection)
    # - Cross-attention k_proj (sensitive based on weight distribution analysis)
    sensitive_matmul_patterns = [
        "/self_attn/q_proj/",
        "/self_attn/k_proj/",
        "/self_attn/v_proj/",
        "/self_attn/out_proj/",
        "/encoder_attn/q_proj/",
        "/encoder_attn/k_proj/",
        "/encoder_attn/v_proj/",
        "/encoder_attn/out_proj/",
        "/fc2/",
    ]

    sensitive = []
    for name in matmul_nodes:
        # proj_out (LM head equivalent) is always sensitive
        if "proj_out" in name:
            sensitive.append(name)
            continue

        # Determine if this is an encoder or decoder node, and extract layer index
        layer_match = re.search(r"layers\.(\d+)", name)
        if not layer_match:
            # Cross-attention KV projections outside layer hierarchy (e.g. /k_proj/MatMul)
            # These are always run once; keep them at INT8 for accuracy
            if any(p.strip("/") in name for p in ["/k_proj/", "/v_proj/"]):
                sensitive.append(name)
            continue

        layer_idx = int(layer_match.group(1))

        is_encoder = "/encoder/" in name
        is_decoder = "/decoder/" in name

        # Check if this layer is in the sensitive set
        if is_encoder and layer_idx in enc_sensitive_layers:
            if any(pat in name for pat in sensitive_matmul_patterns):
                sensitive.append(name)
        elif is_decoder and layer_idx in dec_sensitive_layers:
            if any(pat in name for pat in sensitive_matmul_patterns):
                sensitive.append(name)

    return sensitive

