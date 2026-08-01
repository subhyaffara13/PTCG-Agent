
def is_per_tensor(qscheme):
    return qscheme == torch.per_tensor_affine or qscheme == torch.per_tensor_symmetric

