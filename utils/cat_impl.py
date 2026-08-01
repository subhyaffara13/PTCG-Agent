
def cat_impl(tensors: Sequence[ComplexTensor], dim: int = 0) -> ComplexTensor:
    tensors_r = []
    tensors_i = []

    for t in tensors:
        t_r, t_i = split_complex_arg(t)
        tensors_r.append(t_r)
        tensors_i.append(t_i)

    ret_r = torch.cat(tensors_r, dim=dim)
    ret_i = torch.cat(tensors_i, dim=dim)

    return ComplexTensor(ret_r, ret_i)

