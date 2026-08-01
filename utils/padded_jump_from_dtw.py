
def padded_jump_from_dtw(matrix_2d: torch.Tensor, max_length: torch.Tensor):
    """
    Run Dynamic Time Warping (DTW) on batched tensor
    """
    trace = torch.ops.onnxruntime.DynamicTimeWarping(matrix_2d)
    text_indices = trace[0, :]
    time_indices = trace[1, :]
    jump_times = jump_timings(text_indices, time_indices)
    return F.pad(jump_times, [0, int((max_length - jump_times.size(-1)).item())], mode="constant", value=-1.0)

