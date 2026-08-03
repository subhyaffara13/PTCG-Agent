from typing import Any

def _get_weakref_from_f_locals(
    frame: DynamoFrameType, local_name: str
) -> weakref.ref[Any] | None:
    obj = frame.f_locals.get(local_name, None)
    weak_id = None
    try:
        weak_id = weakref.ref(obj)
    except TypeError:
        pass  # cannot weakref bool object
    return weak_id

