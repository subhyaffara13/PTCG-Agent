
def _infer_name_module(node: nodes.Import, name: str) -> Generator[InferenceResult]:
    context = astroid.context.InferenceContext()
    context.lookupname = name
    return node.infer(context, asname=False)  # type: ignore[no-any-return]

