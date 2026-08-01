
def propagate_nop(node: Node) -> _HandlerRetType:
    def fwd() -> PropagateStatus:
        return _bool_to_status(False)

    def bwd() -> PropagateStatus:
        return _bool_to_status(False)

    return fwd(), bwd()

