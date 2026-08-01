
def _disallow_in_graph_helper(throw_if_not_allowed: bool) -> Callable[..., Any]:
    def inner(fn: Any) -> Any:
        if isinstance(fn, (list, tuple)):
            return [disallow_in_graph(x) for x in fn]
        assert callable(fn), "disallow_in_graph expects a callable"
        if (
            throw_if_not_allowed
            and trace_rules.lookup_callable(fn)
            != variables.TorchInGraphFunctionVariable
            and trace_rules.lookup(fn) != variables.TorchInGraphFunctionVariable
        ):
            raise RuntimeError(
                "disallow_in_graph is expected to be used on an already allowed callable (like torch.* ops). "
                "Allowed callables means callables that TorchDynamo puts as-is in the extracted graph."
            )
        trace_rules._allowed_callable_ids.remove(id(fn))
        trace_rules._nonstrict_trace_callable_ids.remove(id(fn))
        trace_rules._disallowed_callable_ids.add(id(fn))
        return fn

    return inner

