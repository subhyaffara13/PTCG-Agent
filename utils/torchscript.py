
def torchscript(model: Any, example_inputs: Any, verbose: bool = False) -> Any:
    if is_jit_model(model):
        # already done?
        return model

    try:
        return torch.jit.trace(model, example_inputs)
    except Exception:
        try:
            return torch.jit.script(model)
        except Exception:
            if verbose:
                log.exception("jit error")
            else:
                log.error("Both torch.jit.trace and torch.jit.script failed")
    return None


def torchscript(
    gm: torch.fx.GraphModule, fake_tensor_inputs: list[torch.Tensor]
) -> torch.jit.ScriptModule:
    return torch.jit.script(gm)

