
def _raise_autograd_subclass_not_implemented(
    n: fx.Node, desc: AOTInput | AOTOutput
) -> NoReturn:
    raise RuntimeError(
        "Subclasses are currently not supported by this function, but a desugared subclass input "
        f"was found at {n} ({desc}).  The problem is "
        "that there may not necessarily be a 1-1 correspondence between primals/tangents/outputs/grads "
        "when subclasses are involved: for example, the primal might be a plain tensor "
        "but the tangent a tensor subclass that desugared into multiple plain tensors. "
        "It is not clear what exactly you would like this function to do in this case "
        "(Collect all nodes for the subclass together?  Match up the inner nodes if "
        "subclasses match exactly?)  If you have a concrete use case, please file an "
        "issue so we can understand it and design an API that works for your case."
    )

