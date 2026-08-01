
def _has_namedtuple_base(node):
    """Predicate for class inference tip.

    :type node: ClassDef
    :rtype: bool
    """
    return set(node.basenames) & TYPING_NAMEDTUPLE_BASENAMES

