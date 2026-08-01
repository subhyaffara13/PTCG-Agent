
def rebuild_tensor(cls, storage, metadata):
    storage_offset, size, stride, requires_grad = metadata
    t = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
    if cls == torch.nn.parameter.Parameter:
        # we have to pass requires_grad into constructor, rather than set it as an
        # attribute later, because it's an important check for Integer Tensors to
        # have requires_grad=False (or else they raise an error)
        t = torch.nn.parameter.Parameter(t, requires_grad=requires_grad)
    else:
        t.requires_grad = requires_grad
    return t

