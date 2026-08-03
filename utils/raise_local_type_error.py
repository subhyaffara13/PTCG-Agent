from typing import Any

def raise_local_type_error(obj: Any) -> NoReturn:
    raise TypeError(
        f"Type {type(obj)} for object {obj} cannot be saved "
        + "into torch.compile() package since it's defined in local scope. "
        + "Please define the class at global scope (top level of a module)."
    )

