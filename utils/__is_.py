
def __is_(g: jit_utils.GraphContext, self, other):
    if symbolic_helper._is_none(other):
        if symbolic_helper._is_none(self):
            return g.op("Constant", value_t=torch.BoolTensor([1]))
        return g.op("Constant", value_t=torch.BoolTensor([0]))
    return eq(g, self, other)

