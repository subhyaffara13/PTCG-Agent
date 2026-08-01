
def meta_cdist_backward(grad, x1, x2, p, cdist):
    c1 = x1.shape[-1]
    r1 = x1.shape[-2]
    r2 = x2.shape[-2]
    batch_tensor1 = x1.shape[:-2]
    batch_tensor2 = x2.shape[:-2]
    expand_batch_portion = list(torch.broadcast_shapes(batch_tensor1, batch_tensor2))
    tensor1_expand_size = expand_batch_portion.copy()
    tensor1_expand_size.extend([r1, c1])
    batch_product = math.prod(expand_batch_portion)
    if r1 == 0 or r2 == 0 or c1 == 0 or batch_product == 0:
        return torch.zeros_like(x1)
    if tensor1_expand_size != list(x1.shape):
        x1 = x1.expand(tensor1_expand_size)
    return torch.empty_like(x1, memory_format=torch.contiguous_format)

