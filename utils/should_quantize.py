
def should_quantize(node: torch.fx.Node) -> bool:
    allowed_dtypes = get_allowed_dtypes()
    if not is_node_meta_valid(node) or node.meta["val"].dtype not in allowed_dtypes:
        return False
    size_threshold = torch._inductor.config.post_grad_fusion_options[
        "activation_quantization_aten_pass"
    ].get("size_in_mb", 100)
    # calculate the size of the node
    size_in_mb = calculate_tensor_size(node.meta["val"])
    if not torch._inductor.config.post_grad_fusion_options[
        "activation_quantization_aten_pass"
    ].get("skip_dynamo_guards", False):
        return size_in_mb >= size_threshold
    else:
        # case 1: we always quantize tensors with dynamic shapes
        if torch._inductor.config.post_grad_fusion_options[
            "activation_quantization_aten_pass"
        ].get("quantize_dynamic_shape", False):
            return statically_known_true(
                size_in_mb >= size_threshold
            ) or not statically_known_false(size_in_mb >= size_threshold)
        else:
            # case 2: we always not quantize tensors with dynamic shapes
            return statically_known_true(size_in_mb >= size_threshold)

