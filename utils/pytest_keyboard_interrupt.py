
def pytest_keyboard_interrupt(
    excinfo: ExceptionInfo[KeyboardInterrupt | Exit],
) -> None:
    """Called for keyboard interrupt.

    :param excinfo: The exception info.

    Use in conftest plugins
    =======================

    Any conftest plugin can implement this hook.
    """

