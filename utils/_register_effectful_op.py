
def _register_effectful_op(
    op: _op_identifier,
    effect: EffectType | None,
    *,
    lib: Library | None = None,
) -> None:
    r"""
    To specify that an operator has side-effects, we must register an effect
    type for the operator. This will prevent graph passes in torch.compile from
    reordering operations with the same effect type.

    Args:
        op_name: Operator name (along with the overload) or OpOverload object.
        effect: Effect type to register. None means the operator is not effectful.
    """
    if not isinstance(
        op, (str, torch._ops.OpOverload, torch._library.custom_ops.CustomOpDef)
    ):
        raise ValueError(
            f"register_effectful_op({op}): got unexpected type for op: {type(op)}"
        )

    if isinstance(op, torch._ops.OpOverload):
        op = op._name
    opdef = _maybe_get_opdef(op)
    if opdef is not None:
        opdef.register_effect(effect)
    if not isinstance(op, str):
        raise AssertionError(f"op must be str at this point, got {type(op).__name__}")

    namespace, _ = torch._library.utils.parse_namespace(op)
    if lib is None:
        use_lib = Library(namespace, "FRAGMENT")
        _keep_alive.append(use_lib)
    else:
        use_lib = lib
    use_lib._register_effectful_op(op, effect)


def _register_effectful_op(
    op: _op_identifier, effect: EffectType | None
) -> RegistrationHandle:
    qualname = _get_op_qualname(op)
    entry = torch._library.simple_registry.singleton.find(qualname)
    handle = entry.effect.register(effect)
    return handle

