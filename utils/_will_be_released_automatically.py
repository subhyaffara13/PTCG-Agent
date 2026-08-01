
def _will_be_released_automatically(node: nodes.Call) -> bool:
    """Checks if a call that could be used in a ``with`` statement is used in an
    alternative construct which would ensure that its __exit__ method is called.
    """
    callables_taking_care_of_exit = frozenset(
        (
            "contextlib._BaseExitStack.enter_context",
            "contextlib.ExitStack.enter_context",  # necessary for Python 3.6 compatibility
        )
    )
    if not isinstance(node.parent, nodes.Call):
        return False
    func = utils.safe_infer(node.parent.func)
    if not func:
        return False
    return func.qname() in callables_taking_care_of_exit

