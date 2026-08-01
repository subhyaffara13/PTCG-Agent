
def jump_timings(text_indices, time_indices):
    """
    Calculate jump times from text_indices and time_indices where
    text_indices and time_indices are both 1d vectors
    """
    TOKENS_PER_SECOND = 50.0  # noqa: N806
    diff = text_indices[1:] - text_indices[:-1]
    padding = torch.tensor([1], dtype=torch.int32)
    jumps = torch.cat((padding, diff)).to(torch.bool)
    jump_times = time_indices[jumps].to(torch.float) / TOKENS_PER_SECOND
    return jump_times

