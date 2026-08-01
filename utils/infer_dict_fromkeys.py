
def infer_dict_fromkeys(node, context: InferenceContext | None = None):
    """Infer dict.fromkeys.

    :param nodes.Call node: dict.fromkeys() call to infer
    :param context.InferenceContext context: node context
    :rtype nodes.Dict:
        a Dictionary containing the values that astroid was able to infer.
        In case the inference failed for any reason, an empty dictionary
        will be inferred instead.
    """

    def _build_dict_with_elements(elements: list) -> nodes.Dict:
        new_node = nodes.Dict(
            col_offset=node.col_offset,
            lineno=node.lineno,
            parent=node.parent,
            end_lineno=node.end_lineno,
            end_col_offset=node.end_col_offset,
        )
        new_node.postinit(elements)
        return new_node

    call = arguments.CallSite.from_call(node, context=context)
    if call.keyword_arguments:
        raise UseInferenceDefault("TypeError: int() must take no keyword arguments")
    if len(call.positional_arguments) not in {1, 2}:
        raise UseInferenceDefault(
            "TypeError: Needs between 1 and 2 positional arguments"
        )

    default = nodes.Const(None)
    values = call.positional_arguments[0]
    try:
        inferred_values = next(values.infer(context=context))
    except (InferenceError, StopIteration):
        return _build_dict_with_elements([])
    if inferred_values is util.Uninferable:
        return _build_dict_with_elements([])

    # Limit to a couple of potential values, as this can become pretty complicated
    accepted_iterable_elements = (nodes.Const,)
    if isinstance(inferred_values, (nodes.List, nodes.Set, nodes.Tuple)):
        elements = inferred_values.elts
        for element in elements:
            if not isinstance(element, accepted_iterable_elements):
                # Fallback to an empty dict
                return _build_dict_with_elements([])

        elements_with_value = [(element, default) for element in elements]
        return _build_dict_with_elements(elements_with_value)
    if isinstance(inferred_values, nodes.Const) and isinstance(
        inferred_values.value, (str, bytes)
    ):
        elements_with_value = [
            (nodes.Const(element), default) for element in inferred_values.value
        ]
        return _build_dict_with_elements(elements_with_value)
    if isinstance(inferred_values, nodes.Dict):
        keys = inferred_values.itered()
        for key in keys:
            if not isinstance(key, accepted_iterable_elements):
                # Fallback to an empty dict
                return _build_dict_with_elements([])

        elements_with_value = [(element, default) for element in keys]
        return _build_dict_with_elements(elements_with_value)

    # Fallback to an empty dictionary
    return _build_dict_with_elements([])

