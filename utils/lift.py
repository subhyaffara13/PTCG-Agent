
def lift(self: torch.Tensor) -> torch.Tensor:
    return self


def lift(g: jit_utils.GraphContext, self):
    # at::lift() is a no-op from the perspective of tracing for onnx
    return self

