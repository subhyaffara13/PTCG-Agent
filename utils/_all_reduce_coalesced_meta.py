
def _all_reduce_coalesced_meta(self, *args):
    return [torch.empty_like(t) for t in self]

