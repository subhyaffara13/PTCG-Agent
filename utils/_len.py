
def _len(g: jit_utils.GraphContext, self):
    if (
        symbolic_helper._is_tensor_list(self)
        or self.node().kind() == "onnx::SplitToSequence"
    ):
        return g.op("SequenceLength", self)
    sz_0 = size(g, self, g.op("Constant", value_t=torch.LongTensor([0])))
    return symbolic_helper._squeeze_helper(g, sz_0, [0])


def _len(g: jit_utils.GraphContext, self):
    sz_0 = size(g, self, g.op("Constant", value_t=torch.LongTensor([0])))
    return symbolic_helper._squeeze_helper(g, sz_0, [0])

