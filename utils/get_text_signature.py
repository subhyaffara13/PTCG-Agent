
def get_text_signature(fn: FuncIR, *, bound: bool = False) -> str | None:
    """Return a text signature in CPython's internal doc format, or None
    if the function's signature cannot be represented.
    """
    parameters = []
    mark_self = (fn.class_name is not None) and (fn.decl.kind != FUNC_STATICMETHOD) and not bound
    sig = fn.decl.bound_sig if bound and fn.decl.bound_sig is not None else fn.decl.sig
    # Pre-scan for end of positional-only parameters.
    # This is needed to handle signatures like 'def foo(self, __x)', where mypy
    # currently sees 'self' as being positional-or-keyword and '__x' as positional-only.
    pos_only_idx = -1
    for idx, arg in enumerate(sig.args):
        if arg.pos_only and arg.kind in (ArgKind.ARG_POS, ArgKind.ARG_OPT):
            pos_only_idx = idx
    for idx, arg in enumerate(sig.args):
        if arg.name.startswith(("__bitmap", "__mypyc")):
            continue
        kind = (
            inspect.Parameter.POSITIONAL_ONLY
            if idx <= pos_only_idx
            else _ARG_KIND_TO_INSPECT[arg.kind]
        )
        default: object = inspect.Parameter.empty
        if arg.optional:
            default = _find_default_argument(arg.name, fn.blocks)
            if default is _NOT_REPRESENTABLE:
                # This default argument cannot be represented in a __text_signature__
                return None

        curr_param = inspect.Parameter(arg.name, kind, default=default)
        parameters.append(curr_param)
        if mark_self:
            # Parameter.__init__/Parameter.replace do not accept $
            curr_param._name = f"${arg.name}"  # type: ignore[attr-defined]
            mark_self = False
    return f"{fn.name}{inspect.Signature(parameters)}"

