
def create_activation_matching(
    qdq_activations: dict[str, Sequence[numpy.ndarray]],
    float_activations: dict[str, Sequence[numpy.ndarray]] | None = None,
) -> dict[str, dict[str, Sequence[numpy.ndarray]]]:
    """Comparing activation values to help debugging accuracy loss due to quantization.

    This functions takes saved activations from the QDQ model and (optionally) the
    float point model, and provides a data structure for comparing:
        * from the qdq model, activation values before and after QDQ operation
        * across both models, activations from the orignal model vs the corresponding
          activations in the QDQ model

    Arg:
        qdq_activations: Output of `collect_activations`. This must be from a quantized
            model with QDQ format.
        float_activations: Output of `collect_activations`. This must be from the float
            point model.

    Returns:
        Dict for comparing pre and post quantized activation tensors. E.g.
        ```
        qdq_cmp = cmp_qdq_input_output(qdq_activations)
        print(qdq_cmp['activation1']['pre_qdq'][0])
        print(qdq_cmp['activation1'][`post_qdq'][0])


        qdq_cmp = cmp_qdq_input_output(qdq_activations, float_activations)
        print(qdq_cmp['activation1']['float'][0])
        print(qdq_cmp['activation1']['pre_qdq'][0])
        print(qdq_cmp['activation1'][`post_qdq'][0])
        ```
    """

    qdq_cmp: dict[str, dict[str, Sequence[numpy.ndarray]]] = {}
    for tensor_name, tensors in qdq_activations.items():
        if tensor_name.endswith(QUANT_INPUT_SUFFIX):
            pre_name = tensor_name[: -len(QUANT_INPUT_SUFFIX)]
            post_qdq_tensors = qdq_activations.get(pre_name)
            pre_qdq_tensors = tensors
            _add_pre_post_qdq_pair(qdq_cmp, pre_name, pre_qdq_tensors, post_qdq_tensors)
        elif tensor_name.endswith(DEQUANT_OUTPUT_SUFFIX):
            pre_name = tensor_name[: -len(DEQUANT_OUTPUT_SUFFIX)]
            pre_qdq_tensors = qdq_activations.get(pre_name)
            post_qdq_tensors = tensors
            _add_pre_post_qdq_pair(qdq_cmp, pre_name, pre_qdq_tensors, post_qdq_tensors)
        elif tensor_name.endswith(_POST_QDQ_POSTFIX1):
            pre_name = tensor_name[: -len(_POST_QDQ_POSTFIX1)]
            pre_qdq_tensors = qdq_activations.get(pre_name)
            post_qdq_tensors = tensors
            _add_pre_post_qdq_pair(qdq_cmp, pre_name, pre_qdq_tensors, post_qdq_tensors)

    if not float_activations:
        return qdq_cmp

    for act_name, act_values in qdq_cmp.items():
        float_acts = float_activations.get(act_name)
        if float_acts is not None:
            act_values["float"] = float_acts

    return qdq_cmp

