
def _node_names(node: SuccessfulInferenceResult) -> Iterable[str]:
    if not hasattr(node, "locals"):
        return []
    return node.locals.keys()  # type: ignore[no-any-return]

