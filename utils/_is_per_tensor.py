
def _is_per_tensor(qscheme: "torch.qscheme") -> bool:
    return qscheme in [torch.per_tensor_symmetric, torch.per_tensor_affine]

