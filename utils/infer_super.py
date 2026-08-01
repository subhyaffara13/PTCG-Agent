
def infer_super(
    node: nodes.Call, context: InferenceContext | None = None
) -> objects.Super:
    """Understand super calls.

    There are some restrictions for what can be understood:

        * unbounded super (one argument form) is not understood.

        * if the super call is not inside a function (classmethod or method),
          then the default inference will be used.

        * if the super arguments can't be inferred, the default inference
          will be used.
    """
    if len(node.args) == 1:
        # Ignore unbounded super.
        raise UseInferenceDefault

    scope = node.scope()
    if not isinstance(scope, nodes.FunctionDef):
        # Ignore non-method uses of super.
        raise UseInferenceDefault
    if scope.type not in ("classmethod", "method"):
        # Not interested in staticmethods.
        raise UseInferenceDefault

    cls = scoped_nodes.get_wrapping_class(scope)
    assert cls is not None
    if not node.args:
        mro_pointer = cls
        # In we are in a classmethod, the interpreter will fill
        # automatically the class as the second argument, not an instance.
        if scope.type == "classmethod":
            mro_type = cls
        else:
            mro_type = cls.instantiate_class()
    else:
        try:
            mro_pointer = next(node.args[0].infer(context=context))
        except (InferenceError, StopIteration) as exc:
            raise UseInferenceDefault from exc
        try:
            mro_type = next(node.args[1].infer(context=context))
        except (InferenceError, StopIteration) as exc:
            raise UseInferenceDefault from exc

    if isinstance(mro_pointer, util.UninferableBase) or isinstance(
        mro_type, util.UninferableBase
    ):
        # No way we could understand this.
        raise UseInferenceDefault

    super_obj = objects.Super(
        mro_pointer=mro_pointer,
        mro_type=mro_type,
        self_class=cls,
        scope=scope,
        call=node,
    )
    super_obj.parent = node
    return super_obj

