
def fake_global_mask_data(global_mask, batch_size, sequence_length, num_global_tokens):
    """
    Fake data based on the graph input of segment_ids.
    Args:
        segment_ids (TensorProto): graph input of input tensor.
    Returns:
        data (np.array): the data for input tensor
    """
    data_type = global_mask.type.tensor_type.elem_type
    assert data_type in [TensorProto.FLOAT, TensorProto.INT32, TensorProto.INT64]

    if num_global_tokens > 0:
        assert num_global_tokens <= sequence_length
        data = np.zeros((batch_size, sequence_length), dtype=np.int32)
        temp = np.ones((batch_size, num_global_tokens), dtype=np.int32)
        data[: temp.shape[0], : temp.shape[1]] = temp
    else:
        data = np.zeros((batch_size, sequence_length), dtype=np.int32)

    if data_type == TensorProto.FLOAT:
        data = np.float32(data)
    elif data_type == TensorProto.INT64:
        data = np.int64(data)

    return data

