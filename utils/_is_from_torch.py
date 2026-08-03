from typing import Any

def _is_from_torch(obj: Any) -> bool:
    module_name = getattr(obj, "__module__", None)
    if module_name is not None:
        return _torch_but_not_dynamo(module_name) is not None

    name = getattr(obj, "__name__", None)
    # exclude torch because torch.torch.torch.torch works. idk mang
    if name is not None and name != "torch":
        for guess in [torch, torch.nn.functional]:
            if getattr(guess, name, None) is obj:
                return True

    return False

