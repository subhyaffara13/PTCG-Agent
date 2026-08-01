
def fake_input_mask_data(
    input_mask: TensorProto,
    batch_size: int,
    sequence_length: int,
    average_sequence_length: int,
    random_sequence_length: bool,
    mask_type: int = 2,
) -> np.ndarray:
    """Create input tensor based on the graph input of segment_ids.

    Args:
        input_mask (TensorProto): graph input of the attention mask input tensor
        batch_size (int): batch size
        sequence_length (int): sequence length
        average_sequence_length (int): average sequence length excluding paddings
        random_sequence_length (bool): whether use uniform random number for sequence length
        mask_type (int): mask type - 1: mask index (sequence length excluding paddings). Shape is (batch_size).
                                     2: 2D attention mask. Shape is (batch_size, sequence_length).
                                     3: key len, cumulated lengths of query and key. Shape is (3 * batch_size + 2).

    Returns:
        np.ndarray: the input tensor created
    """

    assert input_mask.type.tensor_type.elem_type in [
        TensorProto.FLOAT,
        TensorProto.INT32,
        TensorProto.INT64,
    ]

    if mask_type == 1:  # sequence length excluding paddings
        data = np.ones((batch_size), dtype=np.int32)
        if random_sequence_length:
            for i in range(batch_size):
                data[i] = get_random_length(sequence_length, average_sequence_length)
        else:
            for i in range(batch_size):
                data[i] = average_sequence_length
    elif mask_type == 2:  # 2D attention mask
        data = np.zeros((batch_size, sequence_length), dtype=np.int32)
        if random_sequence_length:
            for i in range(batch_size):
                actual_seq_len = get_random_length(sequence_length, average_sequence_length)
                for j in range(actual_seq_len):
                    data[i, j] = 1
        else:
            temp = np.ones((batch_size, average_sequence_length), dtype=np.int32)
            data[: temp.shape[0], : temp.shape[1]] = temp
    else:
        assert mask_type == 3
        data = np.zeros((batch_size * 3 + 2), dtype=np.int32)
        if random_sequence_length:
            for i in range(batch_size):
                data[i] = get_random_length(sequence_length, average_sequence_length)

            for i in range(batch_size + 1):
                data[batch_size + i] = data[batch_size + i - 1] + data[i - 1] if i > 0 else 0
                data[2 * batch_size + 1 + i] = data[batch_size + i - 1] + data[i - 1] if i > 0 else 0
        else:
            for i in range(batch_size):
                data[i] = average_sequence_length
            for i in range(batch_size + 1):
                data[batch_size + i] = i * average_sequence_length
                data[2 * batch_size + 1 + i] = i * average_sequence_length

    if input_mask.type.tensor_type.elem_type == TensorProto.FLOAT:
        data = np.float32(data)
    elif input_mask.type.tensor_type.elem_type == TensorProto.INT64:
        data = np.int64(data)

    return data

