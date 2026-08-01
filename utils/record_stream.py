
def record_stream(tensor: torch.Tensor, stream_index: int) -> None:
    tensor.record_stream(_get_stream_by_index(stream_index))

