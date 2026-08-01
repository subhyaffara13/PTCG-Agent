
def batch_jump_times(matrix: torch.Tensor, max_decoded_length: torch.Tensor):
    """
    Compute the following to calculate jump times for all batches:
    batched_jump_times = torch.stack([self.padded_jump_from_dtw(matrix[b], max_decoded_length) for b in range(matrix.size(0))])
    """
    list_of_jump_times = []
    for b in range(matrix.size(0)):
        jump_times = padded_jump_from_dtw(matrix[b], max_decoded_length)
        list_of_jump_times.append(jump_times)
    batched_jump_times = torch.stack(list_of_jump_times)
    return batched_jump_times

