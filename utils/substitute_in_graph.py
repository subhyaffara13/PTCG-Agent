
def substitute_in_graph(
    original_fn: Callable[_P, _R],
    *,
    can_constant_fold_through: bool = False,
    skip_signature_check: bool = False,
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """
    Register a polyfill handler for a function, usually a C function from the C extension, to be
    used in place of the original function when inlining the original function in the graph.

    .. note::

        The polyfill handler is only used when inlining the original function. It is not used when
        the original function is called directly. In the eager mode, the decorated function calls
        the performant C function rather than the polyfill handler.

    The polyfill handler is a function that will be called in place of the original function when
    inlining the original function. The polyfill handler should have the same signature and the same
    behavior as the original function.

    Args:
        original_fn (callable): The original function, usually a C function, to register a polyfill
            handler for.
        can_constant_fold_through (bool, optional): Whether the polyfill handler can be constant
            folded through. That is, if the polyfill handler is a pure function and its arguments
            are constant, the result of the polyfill handler can be constant folded during the
            compilation. Defaults to ``False``.
        skip_signature_check (bool, optional): Whether to skip the signature check between the
            original function and the polyfill handler. Defaults to ``False``.

    Returns:
        A decorator that registers the polyfill handler for the original function.

    Example::

        >>> import operator
        >>> operator.indexOf([1, 2, 3, 4, 5], 3)
        2
        >>> torch.compile(operator.indexOf, fullgraph=True)([1, 2, 3, 4, 5], 3)
        ... # xdoctest: +SKIP("Long tracebacks")
        Traceback (most recent call last):
        ...
        torch._dynamo.exc.Unsupported: ...

        >>> @torch.compiler.substitute_in_graph(operator.indexOf)
        ... def indexOf(a, b, /):
        ...     for i, item in enumerate(a):
        ...         if item is b or item == b:
        ...             return i
        ...     raise ValueError("sequence.index(x): x not in sequence")
        >>>
        >>> torch.compile(operator.indexOf, fullgraph=True)([1, 2, 3, 4, 5], 3)
        2
    """
    import torch._dynamo

    return torch._dynamo.substitute_in_graph(
        original_fn,
        can_constant_fold_through=can_constant_fold_through,
        skip_signature_check=skip_signature_check,
    )


def substitute_in_graph(
    original_fn: Callable[_P, _R],
    *,
    can_constant_fold_through: bool = False,
    skip_signature_check: bool = False,
    # type that is embedded in the Python interpreter
    is_embedded_type: bool = False,  # internal use only
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """
    Register a polyfill handler for a function, usually a C function from the C extension, to be
    used in place of the original function when inlining the original function in the graph.

    .. note::

        The polyfill handler is only used when inlining the original function. It is not used when
        the original function is called directly. In the eager mode, the decorated function calls
        the performant C function rather than the polyfill handler.

    The polyfill handler is a function that will be called in place of the original function when
    inlining the original function. The polyfill handler should have the same signature and the same
    behavior as the original function.

    Args:
        original_fn (callable): The original function, usually a C function, to register a polyfill
            handler for.
        can_constant_fold_through (bool, optional): Whether the polyfill handler can be constant
            folded through. That is, if the polyfill handler is a pure function and its arguments
            are constant, the result of the polyfill handler can be constant folded during the
            compilation. Defaults to ``False``.
        skip_signature_check (bool, optional): Whether to skip the signature check between the
            original function and the polyfill handler. Defaults to ``False``.

    Returns:
        A decorator that registers the polyfill handler for the original function.

    Example::

        >>> # xdoctest: +SKIP("conflict with the tests: duplicate polyfill handlers")
        >>> import operator
        >>> operator.indexOf([1, 2, 3, 4, 5], 3)
        2
        >>> torch.compile(operator.indexOf, fullgraph=True)([1, 2, 3, 4, 5], 3)
        Traceback (most recent call last):
        ...
        torch._dynamo.exc.Unsupported: ...

        >>> @torch.compiler.substitute_in_graph(operator.indexOf)
        ... def indexOf(a, b, /):
        ...     for i, item in enumerate(a):
        ...         if item is b or item == b:
        ...             return i
        ...     raise ValueError("sequence.index(x): x not in sequence")
        >>>
        >>> torch.compile(operator.indexOf, fullgraph=True)([1, 2, 3, 4, 5], 3)
        2
    """
    if not is_function(original_fn) and not (
        is_embedded_type and inspect.isclass(original_fn)
    ):
        raise TypeError(
            f"substitute_in_graph expects a function but got {type(original_fn)!r}"
        )
    if is_embedded_type:
        if not inspect.isclass(original_fn):
            raise TypeError(
                f"substitute_in_graph expects a class but got {type(original_fn)!r}"
            )

        from .variables.builder import ITERTOOLS_POLYFILLED_TYPE_IDS, ITERTOOLS_TYPE_IDS

        if id(original_fn) in ITERTOOLS_TYPE_IDS:
            ITERTOOLS_POLYFILLED_TYPE_IDS.add(id(original_fn))

    def wrapper(traceable_fn: Callable[_P, _R]) -> Callable[_P, _R]:
        if not is_function(traceable_fn):
            raise TypeError(
                f"@substitute_in_graph(...) expects a function but got {type(traceable_fn)!r}"
            )

        if not skip_signature_check:
            try:
                original_sig = inspect.signature(original_fn)
            except ValueError:
                pass
            else:
                traceable_sig = inspect.signature(traceable_fn)

                def sig_ident(
                    sig: inspect.Signature,
                ) -> tuple[tuple[str, ...], set[str], dict[str, Any]]:
                    # Ignore annotations for parameters and return type
                    return (
                        tuple(
                            p.name
                            for p in sig.parameters.values()
                            if (
                                p.kind
                                not in {
                                    p.KEYWORD_ONLY,
                                    # the name of *args and **kwargs is not important
                                    p.VAR_POSITIONAL,
                                    p.VAR_KEYWORD,
                                }
                            )
                        ),
                        {
                            p.name
                            for p in sig.parameters.values()
                            if p.kind == p.KEYWORD_ONLY
                        },
                        {
                            p.name: p.default
                            for p in sig.parameters.values()
                            # the name of *args and **kwargs is not important
                            if p.kind not in {p.VAR_POSITIONAL, p.VAR_KEYWORD}
                        },
                    )

                wildcard_sig = inspect.signature(lambda *args, **kwargs: None)

                if (
                    sig_ident(original_sig) != sig_ident(traceable_sig)
                    and sig_ident(original_sig) != sig_ident(wildcard_sig)
                    and sig_ident(traceable_sig) != sig_ident(wildcard_sig)
                ):
                    raise TypeError(
                        f"Signature mismatch between {original_fn} and {traceable_fn}: "
                        f"{original_sig} != {traceable_sig}"
                    )

        from torch._dynamo.guards import GuardBuilder
        from torch._dynamo.trace_rules import (
            _polyfilled_function_ids,
            get_torch_obj_rule_map,
        )
        from torch._dynamo.variables import PolyfilledFunctionVariable
        from torch._dynamo.variables.builder import VariableBuilder

        id_dispatch_map = VariableBuilder._id_dispatch()
        if id(original_fn) in id_dispatch_map:
            raise ValueError(
                f"Duplicate dispatch rule for {original_fn}: "
                "already registered in VariableBuilder's id dispatch map"
            )

        if id(original_fn) in _polyfilled_function_ids:
            raise ValueError(f"Duplicate polyfilled object {original_fn}")

        rule_map: dict[Any, type[VariableTracker]] = get_torch_obj_rule_map()
        if original_fn in rule_map:
            raise ValueError(
                f"Duplicate object {original_fn} with different rules: "
                f"{PolyfilledFunctionVariable}, {rule_map[original_fn]}"
            )

        polyfill_handlers: dict[Callable[..., Any], FunctionType]
        polyfill_handlers = PolyfilledFunctionVariable._get_polyfill_handlers()
        if original_fn in polyfill_handlers:
            raise ValueError(
                f"Duplicate polyfill handlers for {original_fn}: "
                f"already handled by {polyfill_handlers[original_fn]}"
            )

        # Need to wrap the function because we may cannot assign __torch_dynamo_polyfill__ to a
        # C++ function.
        @functools.wraps(traceable_fn)
        def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            return original_fn(*args, **kwargs)

        def dispatch_fn(
            self: VariableBuilder, value: Callable[_P, _R]
        ) -> PolyfilledFunctionVariable:
            if inspect.isclass(value):
                guard_type = GuardBuilder.CLASS_MATCH
            elif inspect.ismodule(value):
                guard_type = GuardBuilder.MODULE_MATCH
            else:
                guard_type = GuardBuilder.ID_MATCH
            guards = self.install_guards(guard_type)
            assert guards is not None
            return PolyfilledFunctionVariable(
                value,
                source=self.source,
                **guards,
            )

        id_dispatch_map[id(original_fn)] = id_dispatch_map[id(wrapped)] = dispatch_fn
        _polyfilled_function_ids.add(id(original_fn))
        _polyfilled_function_ids.add(id(wrapped))
        rule_map[original_fn] = rule_map[wrapped] = PolyfilledFunctionVariable
        polyfill_handlers[original_fn] = polyfill_handlers[wrapped] = wrapped  # type: ignore[assignment]

        wrapped.__torch_dynamo_original__ = original_fn  # type: ignore[attr-defined]
        wrapped.__torch_dynamo_polyfill__ = traceable_fn  # type: ignore[attr-defined]
        wrapped.__torch_dynamo_can_constant_fold_through__ = can_constant_fold_through  # type: ignore[attr-defined]

        return wrapped  # type: ignore[return-value]

    return wrapper

