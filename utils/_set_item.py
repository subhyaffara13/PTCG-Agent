
def _set_item(g: jit_utils.GraphContext, tensor_list, i, v):
    tensor_list = g.op("SequenceErase", tensor_list, i)
    return g.op("SequenceInsert", tensor_list, v, i)

