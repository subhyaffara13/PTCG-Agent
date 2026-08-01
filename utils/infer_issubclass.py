
def infer_issubclass(callnode, context: InferenceContext | None = None):
    """Infer issubclass() calls.

    :param nodes.Call callnode: an `issubclass` call
    :param InferenceContext context: the context for the inference
    :rtype nodes.Const: Boolean Const value of the `issubclass` call
    :raises UseInferenceDefault: If the node cannot be inferred
    """
    call = arguments.CallSite.from_call(callnode, context=context)
    if call.keyword_arguments:
        # issubclass doesn't support keyword arguments
        raise UseInferenceDefault("TypeError: issubclass() takes no keyword arguments")
    if len(call.positional_arguments) != 2:
        raise UseInferenceDefault(
            f"Expected two arguments, got {len(call.positional_arguments)}"
        )
    # The left hand argument is the obj to be checked
    obj_node, class_or_tuple_node = call.positional_arguments

    try:
        obj_type = next(obj_node.infer(context=context))
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc
    if not isinstance(obj_type, nodes.ClassDef):
        raise UseInferenceDefault(
            f"TypeError: arg 1 must be class, not {type(obj_type)!r}"
        )

    # The right hand argument is the class(es) that the given
    # object is to be checked against.
    try:
        class_container = _class_or_tuple_to_container(
            class_or_tuple_node, context=context
        )
    except InferenceError as exc:
        raise UseInferenceDefault from exc
    try:
        issubclass_bool = helpers.object_issubclass(obj_type, class_container, context)
    except AstroidTypeError as exc:
        raise UseInferenceDefault("TypeError: " + str(exc)) from exc
    except MroError as exc:
        raise UseInferenceDefault from exc
    return nodes.Const(issubclass_bool)

