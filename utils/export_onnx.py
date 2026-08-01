
def export_onnx(hf_model: str, cache_dir: str | None, onnx_path_str: str, with_past: bool, opset: int):
    """
    do export
    model: torch model
    onnx_path: where the onnx model saved to
    sample_inputs_tp: inputs for torch model
    """
    model, sample_inputs_tp = initialize_model_and_sample_inputs(hf_model, cache_dir)

    model = move_to_appropriate_device(model, sample_inputs_tp)

    sample_inputs = adapt_inputs_to_device(sample_inputs_tp, next(model.parameters()).device)

    # input_keys would be usesful if the model has some special inputs
    input_keys, onnx_inputs, past_key_value = retrieve_onnx_inputs(model, sample_inputs, with_past)

    onnx_io_tuple = fetch_onnx_inputs_outputs_name(model, onnx_inputs, input_keys, past_key_value, with_past, False)

    onnx_model_name = "model.onnx"
    onnx_path: Path = Path(onnx_path_str).absolute()
    if onnx_path.suffix != ".onnx":
        onnx_path = onnx_path / onnx_model_name

    do_export_internal(model, onnx_io_tuple, onnx_inputs, onnx_path, opset)
    if not with_past:
        return

    onnx_io_tuple = fetch_onnx_inputs_outputs_name(model, onnx_inputs, input_keys, past_key_value, with_past, True)

    onnx_model_name = "model_with_past.onnx"
    onnx_path = onnx_path.parent / onnx_model_name

    do_export_internal(model, onnx_io_tuple, onnx_inputs, onnx_path, opset)

