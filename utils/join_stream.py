
def join_stream(from_index: int, to_index: int) -> None:
    torch.accelerator.set_stream(_get_stream_by_index(to_index))

