import os

def ask_path_exists(message: str, options: Iterable[str]) -> str:
    for action in os.environ.get("PIP_EXISTS_ACTION", "").split():
        if action in options:
            return action
    return ask(message, options)

