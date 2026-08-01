
def update_input_shapes_for_gpt2_decoder_model(decoder_onnx_path: str, use_external_data_format: bool = True):
    """Update the input shapes for the inputs "input_ids" and "position_ids" and make the sequence length dim value 1 for each of them.
       The decoder model will be over-written.

    Args:
        decoder_onnx_path (str): Path of GPT-2 decoder onnx model
        use_external_data_format(bool): output tensors to external data or not.
    """

    decoder_model_proto = onnx.load_model(decoder_onnx_path, load_external_data=True)
    for i in range(len(decoder_model_proto.graph.input)):
        if (
            decoder_model_proto.graph.input[i].name == "input_ids"
            or decoder_model_proto.graph.input[i].name == "position_ids"
        ):
            shape_dim_proto = decoder_model_proto.graph.input[i].type.tensor_type.shape.dim[1]

            # Clear any existing dim_param first
            if shape_dim_proto.HasField("dim_param"):
                shape_dim_proto.Clear()

            # Update dim_value to be 1
            shape_dim_proto.dim_value = 1

    OnnxModel.save(
        decoder_model_proto,
        decoder_onnx_path,
        save_as_external_data=use_external_data_format,
    )
    return True

