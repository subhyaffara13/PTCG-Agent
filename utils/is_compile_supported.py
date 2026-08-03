from typing import Any

def is_compile_supported(device_type: DeviceLikeType) -> Any:
    from .eval_frame import is_dynamo_supported

    type = torch.device(device_type).type
    compile_supported = is_dynamo_supported()
    if type == "cpu":
        pass
    elif type in ["cuda", "xpu", "mtia"] and compile_supported:
        compile_supported = has_triton()
    else:
        compile_supported = False
    return compile_supported

