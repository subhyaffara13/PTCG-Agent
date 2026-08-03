from typing import Any

def get_builtins_dict(global_scope: Scope) -> dict[str, Any]:
    # f_globals["__builtins__"] can be a dict or a module. This is an
    # implementation detail -
    # https://docs.python.org/3/library/builtins.html.

    # This makes guarding on any builtin messy because the guard check_fn
    # has to check if the __builtins__ is a module or dict, and then access
    # by either using getattr or getitem respectively.

    # To solve this problem, we insert a new entry in f_globals which points
    # to the builtins __dict__ and then we guard any builtin on this dict.
    # To avoid any collision with the pre-existing keys, we use the
    # install_global to give us a unique dict key.

    f_builtins = global_scope["__builtins__"]
    if not isinstance(f_builtins, dict):
        f_builtins = f_builtins.__dict__
    return f_builtins

