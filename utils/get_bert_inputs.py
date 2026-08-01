
def get_bert_inputs(
    onnx_file: str,
    input_ids_name: str | None = None,
    segment_ids_name: str | None = None,
    input_mask_name: str | None = None,
) -> tuple[np.ndarray | None, np.ndarray | None, np.ndarray | None]:
    """Find graph inputs for BERT model.
    First, we will deduce inputs from EmbedLayerNormalization node.
    If not found, we will guess the meaning of graph inputs based on naming.

    Args:
        onnx_file (str): onnx model path
        input_ids_name (str, optional): Name of graph input for input IDs. Defaults to None.
        segment_ids_name (str, optional): Name of graph input for segment IDs. Defaults to None.
        input_mask_name (str, optional): Name of graph input for attention mask. Defaults to None.

    Returns:
        Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray]]: input tensors of input_ids,
                                                                                 segment_ids and input_mask
    """
    model = ModelProto()
    with open(onnx_file, "rb") as file:
        model.ParseFromString(file.read())

    onnx_model = OnnxModel(model)
    return find_bert_inputs(onnx_model, input_ids_name, segment_ids_name, input_mask_name)

