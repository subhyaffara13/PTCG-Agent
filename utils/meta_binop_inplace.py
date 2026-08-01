
def meta_binop_inplace(self, other):
    if isinstance(other, torch.Tensor):
        check_inplace_broadcast(self.shape, other.shape)
    return self

