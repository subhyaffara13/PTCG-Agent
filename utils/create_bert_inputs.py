
def create_bert_inputs(
    onnx_model,
    batch_size,
    sequence_length,
    samples,
    input_ids_name=None,
    segment_ids_name=None,
    input_mask_name=None,
):
    """Create dummy inputs for BERT model.

    Args:
        onnx_model (OnnxModel): ONNX model
        batch_size (int): batch size
        sequence_length (int): sequence length
        samples (int): number of samples
        input_ids_name (str, optional): Name of graph input for input IDs. Defaults to None.
        segment_ids_name (str, optional): Name of graph input for segment IDs. Defaults to None.
        input_mask_name (str, optional): Name of graph input for attention mask. Defaults to None.

    Returns:
        List[Dict]: list of inputs
    """
    from bert_test_data import find_bert_inputs, generate_test_data  # noqa: PLC0415

    input_ids, segment_ids, input_mask = find_bert_inputs(onnx_model, input_ids_name, segment_ids_name, input_mask_name)
    all_inputs = generate_test_data(
        batch_size,
        sequence_length,
        test_cases=samples,
        seed=123,
        verbose=False,
        input_ids=input_ids,
        segment_ids=segment_ids,
        input_mask=input_mask,
        random_mask_length=False,
    )

    return all_inputs

