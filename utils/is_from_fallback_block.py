import itertools

def is_from_fallback_block(node: nodes.NodeNG) -> bool:
    """Check if the given node is from a fallback import block."""
    context = find_try_except_wrapper_node(node)
    if not context:
        return False

    if isinstance(context, nodes.ExceptHandler):
        other_body = context.parent.body
        handlers = context.parent.handlers
    else:
        other_body = itertools.chain.from_iterable(
            handler.body for handler in context.handlers
        )
        handlers = context.handlers

    has_fallback_imports = any(
        isinstance(import_node, (nodes.ImportFrom, nodes.Import))
        for import_node in other_body
    )
    ignores_import_error = _except_handlers_ignores_exceptions(
        handlers, (ImportError, ModuleNotFoundError)
    )
    return ignores_import_error or has_fallback_imports

