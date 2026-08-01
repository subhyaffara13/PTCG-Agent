
def get_sample_segment_length(
    device: torch.device,
    segment_length: int,
    use_int32: bool = False,
):
    torch_dtype = torch.int32 if use_int32 else torch.int64
    segment_size = torch.tensor([segment_length], device=device, dtype=torch_dtype)
    return segment_size

