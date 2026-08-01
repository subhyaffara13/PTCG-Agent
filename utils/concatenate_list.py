
def concatenate_list(input_list):
    if isinstance(input_list[0], list):
        return [item for sublist in input_list for item in sublist]
    elif isinstance(input_list[0], np.ndarray):
        return np.concatenate(input_list, axis=0)
    elif isinstance(input_list[0], torch.Tensor):
        return torch.cat(input_list, dim=0)

