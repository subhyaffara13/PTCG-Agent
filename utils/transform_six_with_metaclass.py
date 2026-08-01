
def transform_six_with_metaclass(node):
    """Check if the given class node is defined with *six.with_metaclass*.

    If so, inject its argument as the metaclass of the underlying class.
    """
    call = node.bases[0]
    node._metaclass = call.args[0]
    return node

