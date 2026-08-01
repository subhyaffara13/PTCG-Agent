
def nonzero_numpy(
    fake_mode: FakeTensorMode, func: OpOverload, arg: FakeTensor
) -> list[FakeTensor]:
    return torch.ops.aten.nonzero.default(arg).unbind(1)


def nonzero_numpy(g: jit_utils.GraphContext, input, _outputs=None):
    return unbind(g, opset9.nonzero(g, input), 1, _outputs=_outputs)


def nonzero_numpy(g: jit_utils.GraphContext, input, _outputs=None):
    return unbind(g, nonzero(g, input), 1, _outputs=_outputs)

