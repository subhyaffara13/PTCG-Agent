
def is_floating_point(g: jit_utils.GraphContext, self):
    if symbolic_helper._is_fp(self):
        return g.op("Constant", value_t=torch.BoolTensor([1]))
    return g.op("Constant", value_t=torch.BoolTensor([0]))

