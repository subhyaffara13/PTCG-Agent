
def is_postponed_evaluation_enabled(node: nodes.NodeNG) -> bool:
    """Check if the postponed evaluation of annotations is enabled."""
    module = node.root()
    return "annotations" in module.future_imports

