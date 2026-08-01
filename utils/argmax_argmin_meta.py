
def argmax_argmin_meta(self, dim=None, keepdim=False):
    check_argmax_argmin("argmax", self, dim)
    dims = utils.reduction_dims(self.shape, (dim,) if dim is not None else None)
    shape = _compute_reduction_shape(self, dims, keepdim)
    return self.new_empty(shape, dtype=torch.int64)

