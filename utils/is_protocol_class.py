
def is_protocol_class(cls: nodes.NodeNG) -> bool:
    """Check if the given node represents a protocol class.

    :param cls: The node to check
    :returns: True if the node is or inherits from typing.Protocol directly, false otherwise.
    """
    if not isinstance(cls, nodes.ClassDef):
        return False

    # Return if klass is protocol
    if cls.qname() in TYPING_PROTOCOLS:
        return True

    for base in cls.bases:
        try:
            for inf_base in base.infer():
                if inf_base.qname() in TYPING_PROTOCOLS:
                    return True
        except astroid.InferenceError:
            continue
    return False

