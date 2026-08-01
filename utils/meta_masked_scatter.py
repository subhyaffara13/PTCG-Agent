
def meta_masked_scatter(self, mask, source):
    self, mask = _maybe_broadcast(self, mask)
    output = torch.empty_like(self, memory_format=torch.contiguous_format)
    return meta_masked_scatter_(output, mask, source)

