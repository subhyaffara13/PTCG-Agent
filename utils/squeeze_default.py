
def squeeze_default(self: Tensor, dim: int | None = None):
    # handle a scalar directly
    if not isinstance(self, torch.Tensor):
        return self
    # perform squeeze
    if dim is None:
        return aten.squeeze.dims(self, list(range(self.dim())))
    else:
        return aten.squeeze.dims(self, [dim])

