
def is_terminating_func(node: nodes.Call) -> bool:
    """Detect call to exit(), quit(), os._exit(), sys.exit(), or
    functions annotated with `typing.NoReturn` or `typing.Never`.
    """
    if not isinstance(node.func, (nodes.Attribute, nodes.Name)) or isinstance(
        node.parent, nodes.Lambda
    ):
        return False

    try:
        for inferred in node.func.infer():
            if (
                hasattr(inferred, "qname")
                and inferred.qname() in TERMINATING_FUNCS_QNAMES
            ):
                return True
            match inferred:
                case astroid.BoundMethod(_proxied=astroid.UnboundMethod(_proxied=p)):
                    # Unwrap to get the actual function node object
                    inferred = p
            if (  # pylint: disable=too-many-boolean-expressions
                isinstance(inferred, nodes.FunctionDef)
                and (
                    not isinstance(inferred, nodes.AsyncFunctionDef)
                    or isinstance(node.parent, nodes.Await)
                )
                and isinstance(inferred.returns, nodes.Name)
                and (inferred_func := safe_infer(inferred.returns))
                and hasattr(inferred_func, "qname")
                and inferred_func.qname()
                in (
                    *TYPING_NEVER,
                    *TYPING_NORETURN,
                    # In Python 3.7 - 3.8, NoReturn is alias of '_SpecialForm'
                    # "typing._SpecialForm",
                    # But 'typing.Any' also inherits _SpecialForm
                    # See #9751
                )
            ):
                return True
    except (StopIteration, astroid.InferenceError):
        pass

    return False

