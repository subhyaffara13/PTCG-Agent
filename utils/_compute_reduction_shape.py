
def _compute_reduction_shape(self, dims, keepdim):
    if keepdim:
        return tuple(self.shape[i] if i not in dims else 1 for i in range(self.ndim))

    return utils.compute_reduction_output_shape(self.shape, dims)

