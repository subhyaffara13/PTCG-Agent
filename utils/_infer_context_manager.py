
def _infer_context_manager(self, mgr, context):
    try:
        inferred = next(mgr.infer(context=context))
    except StopIteration as e:
        raise InferenceError(node=mgr) from e
    if isinstance(inferred, bases.Generator):
        # Check if it is decorated with contextlib.contextmanager.
        func = inferred.parent
        if not func.decorators:
            raise InferenceError(
                "No decorators found on inferred generator %s", node=func
            )

        for decorator_node in func.decorators.nodes:
            decorator = next(decorator_node.infer(context=context), None)
            if isinstance(decorator, nodes.FunctionDef):
                if decorator.qname() == _CONTEXTLIB_MGR:
                    break
        else:
            # It doesn't interest us.
            raise InferenceError(node=func)
        try:
            yield next(inferred.infer_yield_types())
        except StopIteration as e:
            raise InferenceError(node=func) from e

    elif isinstance(inferred, bases.Instance):
        try:
            enter = next(inferred.igetattr("__enter__", context=context))
        except (InferenceError, AttributeInferenceError, StopIteration) as exc:
            raise InferenceError(node=inferred) from exc
        if not isinstance(enter, bases.BoundMethod):
            raise InferenceError(node=enter)
        yield from enter.infer_call_result(self, context)
    else:
        raise InferenceError(node=mgr)

