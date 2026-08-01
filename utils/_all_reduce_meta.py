
def _all_reduce_meta(self, *args):
    return torch.empty_like(self, memory_format=torch.contiguous_format)

