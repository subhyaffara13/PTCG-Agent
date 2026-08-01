
def _register_quantization_weight_pack_pass():
    # Step 1: Dequant promotion for int8-mixed-fp32/bf16
    _register_dequant_promotion()

    # Step 2: QConv weight prepack
    _register_qconv_weight_prepack()

    # Step 3: QLinear weight prepack
    _register_qlinear_weight_prepack()
    _register_linear_dynamic_fp16_weight_prepack()

    # Step 4: weight prepack for SmoothQuant from Torchao
    _register_smooth_quant_int_mm_pattern()

    # Step 5: QLinear post op Fusion
    if not torch.ops.mkldnn._is_mkldnn_acl_supported():
        # skip fusion on ARM
        _register_qconv_unary_fusion()
        _register_qconv_binary_fusion()
        _register_qlinear_unary_fusion()
        _register_qlinear_binary_fusion()

