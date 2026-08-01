
def fake_segment_ids_data(segment_ids: TensorProto, batch_size: int, sequence_length: int) -> np.ndarray:
    """Create input tensor based on the graph input of segment_ids

    Args:
        segment_ids (TensorProto): graph input of the token_type_ids input tensor
        batch_size (int): batch size
        sequence_length (int): sequence length

    Returns:
        np.ndarray: the input tensor created
    """
    assert segment_ids.type.tensor_type.elem_type in [
        TensorProto.FLOAT,
        TensorProto.INT32,
        TensorProto.INT64,
    ]

    data = np.zeros((batch_size, sequence_length), dtype=np.int32)

    if segment_ids.type.tensor_type.elem_type == TensorProto.FLOAT:
        data = np.float32(data)
    elif segment_ids.type.tensor_type.elem_type == TensorProto.INT64:
        data = np.int64(data)

    return data

