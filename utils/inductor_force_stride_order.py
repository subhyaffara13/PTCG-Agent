
def inductor_force_stride_order(input_tensor, stride):
    stride_order = ir.get_stride_order(stride)
    return ir.ExternKernel.require_stride_order(input_tensor, stride_order)

