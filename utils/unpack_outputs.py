from typing import Any

def unpack_outputs(outputs: tuple[Any, ...]) -> tuple[Any, Any]:
    out_dims = outputs[-1]
    if isinstance(out_dims, tuple):
        outputs = outputs[:-1]
    else:
        outputs = outputs[0]
    return outputs, out_dims

