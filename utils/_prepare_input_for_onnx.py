
def _prepare_input_for_onnx(
    args, kwargs, remained_onnx_input_idx: Sequence[int] | None, flatten: bool
):
    """Prepare input for ONNX model execution in ONNX backend.

    Any future changes/formatting to the input before dispatching to the ONNX backend
    run should be made in this function.

    Args:
        args: positional arguments for PyTorch model forward method.
        kwargs: keyword arguments for PyTorch model forward method.
        remained_onnx_input_idx: indices of inputs to be used for ONNX model execution.
        flatten: whether to flatten the input before dispatching to the ONNX model execution.

    Returns:
        onnx_inputs: positional arguments for ONNX model execution in ONNX backend.
    """
    onnx_inputs = _prepare_input_for_export(args, kwargs)
    if flatten:
        onnx_inputs, _ = torch.jit._flatten(onnx_inputs)
    elif onnx_inputs and onnx_inputs[-1] == {}:
        # Handle empty kwargs (normally removed by flatten).
        onnx_inputs = onnx_inputs[:-1]
    if remained_onnx_input_idx is not None:
        return [onnx_inputs[i] for i in remained_onnx_input_idx]
    else:
        return onnx_inputs

