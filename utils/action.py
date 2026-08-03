from typing import Callable

def action(subparser: argparse.ArgumentParser) -> Callable[[ActionFunction], ActionFunction]:
    """Decorator to tie an action function to a subparser."""

    def register(func: ActionFunction) -> ActionFunction:
        subparser.set_defaults(action=func)
        return func

    return register

