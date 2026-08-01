
def fake_input_ids_data(
    input_ids: TensorProto, batch_size: int, sequence_length: int, dictionary_size: int
) -> np.ndarray:
    """Create input tensor based on the graph input of input_ids

    Args:
        input_ids (TensorProto): graph input of the input_ids input tensor
        batch_size (int): batch size
        sequence_length (int): sequence length
        dictionary_size (int): vocabulary size of dictionary

    Returns:
        np.ndarray: the input tensor created
    """
    assert input_ids.type.tensor_type.elem_type in [
        TensorProto.FLOAT,
        TensorProto.INT32,
        TensorProto.INT64,
    ]

    data = np.random.randint(dictionary_size, size=(batch_size, sequence_length), dtype=np.int32)

    if input_ids.type.tensor_type.elem_type == TensorProto.FLOAT:
        data = np.float32(data)
    elif input_ids.type.tensor_type.elem_type == TensorProto.INT64:
        data = np.int64(data)

    return data

