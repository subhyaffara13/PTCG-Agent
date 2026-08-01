
def infer_all(
    node: nodes.NodeNG, context: InferenceContext | None = None
) -> list[InferenceResult]:
    try:
        return list(node.infer(context=context))
    except astroid.InferenceError:
        return []
    except Exception as e:  # pragma: no cover
        raise AstroidError from e

