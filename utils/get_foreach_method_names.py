
def get_foreach_method_names(name):
    # get torch inplace reference function
    op_name = "_foreach_" + name
    inplace_op_name = op_name + "_"

    op = getattr(torch, op_name, None)
    inplace_op = getattr(torch, inplace_op_name, None)

    ref = getattr(torch, name, None)
    ref_inplace = getattr(torch.Tensor, name + "_", None)
    return op, inplace_op, ref, ref_inplace

