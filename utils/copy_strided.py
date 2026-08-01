
def copy_strided(x, stride):
    stride = V.graph.sizevars.guarding_hints_or_throw(stride)
    stride_order = sorted(range(len(stride)), key=stride.__getitem__)
    return ir.ExternKernel.require_stride_order(x, stride_order)

