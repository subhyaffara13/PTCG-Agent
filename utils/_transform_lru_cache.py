
def _transform_lru_cache(node, context: InferenceContext | None = None) -> None:
    # TODO: this is not ideal, since the node should be immutable,
    # but due to https://github.com/pylint-dev/astroid/issues/354,
    # there's not much we can do now.
    # Replacing the node would work partially, because,
    # in pylint, the old node would still be available, leading
    # to spurious false positives.
    node.special_attributes = LruWrappedModel()(node)

