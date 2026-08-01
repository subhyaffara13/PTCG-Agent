
def meta_weight_norm_backward(grad_w, saved_v, saved_g, saved_norms, dim):
    grad_v = torch.empty_like(saved_v)
    grad_g = torch.empty_like(saved_g)
    return grad_v, grad_g

