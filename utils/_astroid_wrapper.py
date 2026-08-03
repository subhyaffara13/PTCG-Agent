from typing import Callable

def _astroid_wrapper(
    func: Callable[[str], nodes.Module],
    modname: str,
    verbose: bool = False,
) -> nodes.Module | None:
    if verbose:
        print(f"parsing {modname}...")
    try:
        return func(modname)
    except astroid.exceptions.AstroidBuildingError as exc:
        print(exc)
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
    return None

