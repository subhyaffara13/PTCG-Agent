
def infer_isinstance(
    callnode: nodes.Call, context: InferenceContext | None = None
) -> nodes.Const:
    """Infer isinstance calls.

    :param nodes.Call callnode: an isinstance call
    :raises UseInferenceDefault: If the node cannot be inferred
    """
    call = arguments.CallSite.from_call(callnode, context=context)
    if call.keyword_arguments:
        # isinstance doesn't support keyword arguments
        raise UseInferenceDefault("TypeError: isinstance() takes no keyword arguments")
    if len(call.positional_arguments) != 2:
        raise UseInferenceDefault(
            f"Expected two arguments, got {len(call.positional_arguments)}"
        )
    # The left hand argument is the obj to be checked
    obj_node, class_or_tuple_node = call.positional_arguments
    # The right hand argument is the class(es) that the given
    # obj is to be check is an instance of
    try:
        class_container = _class_or_tuple_to_container(
            class_or_tuple_node, context=context
        )
    except InferenceError as exc:
        raise UseInferenceDefault from exc
    try:
        isinstance_bool = helpers.object_isinstance(obj_node, class_container, context)
    except AstroidTypeError as exc:
        raise UseInferenceDefault("TypeError: " + str(exc)) from exc
    except MroError as exc:
        raise UseInferenceDefault from exc
    if isinstance(isinstance_bool, util.UninferableBase):
        raise UseInferenceDefault
    return nodes.Const(isinstance_bool)

