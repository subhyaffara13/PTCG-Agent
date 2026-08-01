
def get_sample_sot_sequence_length(
    device: torch.device,
    sot_sequence_length: int,
    use_int32: bool = False,
):
    torch_dtype = torch.int32 if use_int32 else torch.int64
    sot_length = torch.tensor([sot_sequence_length], device=device, dtype=torch_dtype)
    return sot_length

