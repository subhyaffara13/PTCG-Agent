from typing import Callable

def builtins_wrapper(
    func: Callable[[DataDrivenTestCase], None], path: str
) -> Callable[[DataDrivenTestCase], None]:
    """Decorate a function that implements a data-driven test case to copy an
    alternative builtins module implementation in place before performing the
    test case. Clean up after executing the test case.
    """
    return lambda testcase: perform_test(func, path, testcase)

