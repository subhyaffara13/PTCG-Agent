
def _get_sdpa_extreme_seqlen(func, tensor):
    return int(func(tensor).item())

