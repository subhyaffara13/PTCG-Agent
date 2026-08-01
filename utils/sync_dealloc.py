
def sync_dealloc(
    wait_event_index: int, src_stream_index: int, to_dealloc: torch.Tensor
) -> None:
    """An op which waits on an event and moves the last usage of to_dealloc
    after the wait, so that after the sync occurs, the deallocation or
    subsequent reuse of the tensor's memory will be guaranteed to happen
    after a side stream is finished using it.
    See https://docs.pytorch.org/docs/stable/generated/torch.Tensor.record_stream.html#torch.Tensor.record_stream
    for more details"""
    torch.ops.streams.wait_event.default(wait_event_index, src_stream_index)

