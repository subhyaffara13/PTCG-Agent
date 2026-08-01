
def _reg(symbolic_fn: typing.Callable, namespace: str = "aten"):
    name = f"{namespace}::{symbolic_fn.__name__}"
    torch.onnx.register_custom_op_symbolic(name, symbolic_fn, _OPSET_VERSION)
    _registered_ops.add(name)

