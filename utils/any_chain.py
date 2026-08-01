
def any_chain(*op_support: OperatorSupportBase) -> OperatorSupportBase:
    """Combines a sequence of `OperatorSupportBase` instances to form a single `OperatorSupportBase`
    instance by evaluating each input `OperatorSupportBase` instance, and returns True if
    any of it reports True.
    """

    def _any_chain(submods, node) -> bool:
        return any(x.is_node_supported(submods, node) for x in op_support)

    return create_op_support(_any_chain)

