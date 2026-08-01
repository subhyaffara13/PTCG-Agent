
def _is_tensor_irnode(x):
    return isinstance(x, ir.IRNode) and not isinstance(
        x, (ir.NonTensorObj, ir.OpaqueMultiOutput)
    )

