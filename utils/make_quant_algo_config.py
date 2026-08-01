
def make_quant_algo_config(
    precision: Precision,
    quant_method: str,
    matmul_nodes: list[str] | None = None,
    encoder_layers: int = 0,
    decoder_layers: int = 0,
):
    """Create quantization algorithm config for Whisper models.

    Args:
        precision: Precision enum (INT4 or INT8).
        quant_method: "k_quant" or "k_quant_mixed".
        matmul_nodes: list of MatMul node names from the ONNX graph.
        encoder_layers: number of encoder layers (needed for k_quant_mixed).
        decoder_layers: number of decoder layers (needed for k_quant_mixed).

    Returns:
        KQuantWeightOnlyQuantConfig with appropriate customized_weight_config.
    """
    customized_weight_config = {}

    if precision == Precision.INT8:
        # INT8: set every MatMul to 8-bit
        for node_name in matmul_nodes:
            customized_weight_config[node_name] = {"bits": 8}
    elif precision == Precision.INT4 and quant_method == "k_quant_mixed":
        # k_quant_mixed: sensitive layers at INT8, rest at INT4
        sensitive_names = get_sensitive_node_names(matmul_nodes, encoder_layers, decoder_layers)
        for node_name in sensitive_names:
            customized_weight_config[node_name] = {"bits": 8}
        logger.info(
            f"k_quant_mixed: {len(sensitive_names)} sensitive nodes (INT8) "
            f"out of {len(matmul_nodes)} total MatMul nodes"
        )
        for name in sensitive_names:
            logger.info(f"  INT8: {name}")

    return KQuantWeightOnlyQuantConfig(customized_weight_config=customized_weight_config)

