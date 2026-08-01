
def _infer_object__new__decorator(
    node: nodes.ClassDef, context: InferenceContext | None = None, **kwargs: Any
) -> Iterator[Instance]:
    # Instantiate class immediately
    # since that's what @object.__new__ does
    return iter((node.instantiate_class(),))

