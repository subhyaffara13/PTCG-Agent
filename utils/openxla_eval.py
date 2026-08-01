
def openxla_eval(
    model: fx.GraphModule, fake_tensor_inputs: list[torch.Tensor]
) -> CompiledFn:
    return xla_backend_helper(model, fake_tensor_inputs, boxed=False)

