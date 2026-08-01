
def _args_kwargs_to_normalized_args_kwargs(
    sig: inspect.Signature,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    normalize_to_only_use_kwargs: bool,
) -> ArgsKwargsPair | None:
    """
    Given a call target, args, and kwargs, return the arguments normalized into
    an ArgsKwargsPair, or None if the type signature is not supported by
    this normalization.

    Args:

        sig (inspect.Signature): Signature object for the target
        args (Tuple): Arguments that appear at the callsite for `target`
        kwargs (Dict): Keyword arguments that appear at the callsite for `target`
        normalize_to_only_use_kwargs (bool): Whether to normalize to only use kwargs.

    Returns:

        Optional[ArgsKwargsPair]: Normalized args and kwargs for `target`, or `None` if
            this target is not supported.
    """

    # Don't currently support positional-only
    # or varargs (*args, **kwargs) signatures
    supported_parameter_types = {
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        inspect.Parameter.KEYWORD_ONLY,
    }
    if any(p.kind not in supported_parameter_types for p in sig.parameters.values()):
        # Add an exception for one signature, which is common for random/uniform, i.e.:
        # Tensor(a!) self, float from=0, float to=1, *, Generator? generator=None
        # `from` is Python keyword and as such functions with that signature should have
        # positional-only args, but at the same time they could be dispatched as kwargs
        if list(sig.parameters.keys()) != ["input", "from", "to", "generator"]:
            return None

    bound_args = _fast_bind(sig, *args, **kwargs)
    bound_args.apply_defaults()

    new_kwargs: dict[str, Any] = {}
    new_args: list[Any] = []
    for i, param in enumerate(sig.parameters):
        if not normalize_to_only_use_kwargs and i < len(args):
            new_args.append(bound_args.arguments[param])
        else:
            new_kwargs[param] = bound_args.arguments[param]

    return ArgsKwargsPair(tuple(new_args), new_kwargs)

