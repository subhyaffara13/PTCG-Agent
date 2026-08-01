
def resize_as(self, other, memory_format=None):
    if memory_format is None:
        memory_format = torch.contiguous_format
    if memory_format == torch.preserve_format:
        memory_format = suggest_memory_format(other)
    return aten.resize(self, other.shape, memory_format=memory_format)

