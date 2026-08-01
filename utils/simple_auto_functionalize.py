
def simple_auto_functionalize(x, z):
    return torch.ops.testlib.mutating_custom_op(x, z)

