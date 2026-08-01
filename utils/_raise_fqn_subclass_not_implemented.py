
def _raise_fqn_subclass_not_implemented(
    n: fx.Node, desc: AOTInput | AOTOutput
) -> NoReturn:
    raise RuntimeError(
        "Subclasses are currently not supported by this function, but a desugared subclass input "
        f"was found at {n} ({desc}).  The problem is "
        "that there may not necessarily be a 1-1 correspondence between a FQN and a plain tensor "
        "when subclasses are involved: for example, a parameter that is a subclass "
        "would desugar into multiple plain tensors, which we can't uniquely assign the "
        "FQN to.  It's not clear what you want the API to do in this case: do you want to "
        "instead return a struct of nodes showing how to assemble the subclass?  But you "
        "don't (directly) have the metadata for the subclass?  If you have a concrete use "
        "case, please file an issue so we can understand it and design an API that works for your case."
    )

