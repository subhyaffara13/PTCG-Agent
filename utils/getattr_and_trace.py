from typing import Any

def getattr_and_trace(*args: Any, **kwargs: Any) -> Any:
    wrapper_obj = args[0]
    attr_name = args[1]
    fn = getattr(wrapper_obj, attr_name)
    return fn(*args[2:], **kwargs)

