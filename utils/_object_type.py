
def _object_type(
    node: InferenceResult, context: InferenceContext | None = None
) -> Generator[InferenceResult | None]:
    astroid_manager = manager.AstroidManager()
    builtins = astroid_manager.builtins_module
    context = context or InferenceContext()

    for inferred in node.infer(context=context):
        if isinstance(inferred, scoped_nodes.ClassDef):
            metaclass = inferred.metaclass(context=context)
            if metaclass:
                yield metaclass
                continue
            yield builtins.getattr("type")[0]
        elif isinstance(
            inferred,
            (scoped_nodes.Lambda, bases.UnboundMethod, scoped_nodes.FunctionDef),
        ):
            yield _function_type(inferred, builtins)
        elif isinstance(inferred, scoped_nodes.Module):
            yield _build_proxy_class("module", builtins)
        elif isinstance(inferred, nodes.Unknown):
            raise InferenceError
        elif isinstance(inferred, util.UninferableBase):
            yield inferred
        elif isinstance(inferred, (bases.Proxy, nodes.Slice, objects.Super)):
            yield inferred._proxied
        else:  # pragma: no cover
            raise AssertionError(f"We don't handle {type(inferred)} currently")

