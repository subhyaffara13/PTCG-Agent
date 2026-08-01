
def _functools_partial_inference(
    node: nodes.Call, context: InferenceContext | None = None
) -> Iterator[objects.PartialFunction]:
    call = arguments.CallSite.from_call(node, context=context)
    number_of_positional = len(call.positional_arguments)
    if number_of_positional < 1:
        raise UseInferenceDefault("functools.partial takes at least one argument")
    if number_of_positional == 1 and not call.keyword_arguments:
        raise UseInferenceDefault(
            "functools.partial needs at least to have some filled arguments"
        )

    partial_function = call.positional_arguments[0]
    try:
        inferred_wrapped_function = next(partial_function.infer(context=context))
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc
    if isinstance(inferred_wrapped_function, UninferableBase):
        raise UseInferenceDefault("Cannot infer the wrapped function")
    if not isinstance(inferred_wrapped_function, nodes.FunctionDef):
        raise UseInferenceDefault("The wrapped function is not a function")

    # Determine if the passed keywords into the callsite are supported
    # by the wrapped function.
    if not inferred_wrapped_function.args:
        function_parameters = []
    else:
        function_parameters = chain(
            inferred_wrapped_function.args.args or (),
            inferred_wrapped_function.args.posonlyargs or (),
            inferred_wrapped_function.args.kwonlyargs or (),
        )
    parameter_names = {
        param.name
        for param in function_parameters
        if isinstance(param, nodes.AssignName)
    }
    if set(call.keyword_arguments) - parameter_names:
        raise UseInferenceDefault("wrapped function received unknown parameters")

    partial_function = objects.PartialFunction(
        call,
        name=inferred_wrapped_function.name,
        lineno=inferred_wrapped_function.lineno,
        col_offset=inferred_wrapped_function.col_offset,
        parent=node.parent,
    )
    partial_function.postinit(
        args=inferred_wrapped_function.args,
        body=inferred_wrapped_function.body,
        decorators=inferred_wrapped_function.decorators,
        returns=inferred_wrapped_function.returns,
        type_comment_returns=inferred_wrapped_function.type_comment_returns,
        type_comment_args=inferred_wrapped_function.type_comment_args,
        doc_node=inferred_wrapped_function.doc_node,
    )
    return iter((partial_function,))

