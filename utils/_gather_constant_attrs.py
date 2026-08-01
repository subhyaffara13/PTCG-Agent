
def _gather_constant_attrs(m: torch.nn.Module) -> ConstantAttrMap:
    """Search the module hierarchy, gathering up all tensor and ScriptObject constants.

    Returns a dictionary mapping hash(value) to the name of the constant. We
    have to abuse `hash` here unfortunately, see: [ScriptObject hash].
    """
    constants = ConstantAttrMap()
    buffers_parameters = set(m.buffers())
    buffers_parameters.update(m.parameters())

    def inner(m: torch.nn.Module, prefix_atoms: list[str], constants):
        for k, v in m.__dict__.items():
            if isinstance(
                v,
                (
                    torch.Tensor,
                    torch.ScriptObject,
                    FakeScriptObject,
                ),
            ):
                if v in buffers_parameters:
                    # filter out buffers and parameters, leaving only constants
                    continue

                fqn = ".".join(prefix_atoms + [k])
                constants.add(v, fqn)
        for k, v in m.named_children():
            inner(v, prefix_atoms + [k], constants)

    inner(m, [], constants)
    return constants

