from typing import Any

def _combine_args(f, args, kwargs) -> dict[str, Any]:
    # combine args and kwargs following the signature of f, as it happens
    # in the body of f when called with *args, **kwargs
    if isinstance(f, ExportedProgram):
        f = f.module()

    signature = (
        inspect.signature(f.forward)
        if isinstance(f, torch.nn.Module)
        else inspect.signature(f)
    )
    kwargs = kwargs if kwargs is not None else {}
    return signature.bind(*args, **kwargs).arguments

