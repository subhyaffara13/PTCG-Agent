
def meta__adaptive_avg_pool3d_backward(grad_output, self):
    _adaptive_pool_empty_output_check(grad_output, "adaptive_avg_pool3d_backward")
    return torch.empty_like(self, memory_format=torch.legacy_contiguous_format)

