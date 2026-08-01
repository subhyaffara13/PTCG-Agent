
def _dequantize_tensor_list(tensor_list, qtype, quant_loss=None):
    if not isinstance(tensor_list, list) or not all(
        isinstance(p, torch.Tensor) for p in tensor_list
    ):
        raise RuntimeError(
            f"_dequantize_tensor_list expecting list of torch.Tensor as input but found {type(tensor_list)}"
        )
    dequantized_tensor_list = [_dequantize_tensor(t, qtype) for t in tensor_list]
    return dequantized_tensor_list


def _dequantize_tensor_list(t: Any) -> Any:
    return (
        [_dequantize_tensor_list(x) for x in t]
        if type(t) is list
        else t.dequantize()
        if t.is_quantized
        else t
    )

