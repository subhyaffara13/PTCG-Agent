from typing import Callable

def only_required_for_messages(
    *messages: str,
) -> Callable[
    [AstCallbackMethod[_CheckerT, _NodeT]], AstCallbackMethod[_CheckerT, _NodeT]
]:
    """Decorator to store messages that are handled by a checker method as an
    attribute of the function object.

    This information is used by ``ASTWalker`` to decide whether to call the decorated
    method or not. If none of the messages is enabled, the method will be skipped.
    Therefore, the list of messages must be well maintained at all times!
    This decorator only has an effect on ``visit_*`` and ``leave_*`` methods
    of a class inheriting from ``BaseChecker``.
    """

    def store_messages(
        func: AstCallbackMethod[_CheckerT, _NodeT],
    ) -> AstCallbackMethod[_CheckerT, _NodeT]:
        func.checks_msgs = messages  # type: ignore[attr-defined]
        return func

    return store_messages

