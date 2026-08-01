
def _rand_eager_offsets_meta(offsets, device: torch.device):
    return torch.empty((len(offsets), 2), dtype=torch.int64, device=device)

