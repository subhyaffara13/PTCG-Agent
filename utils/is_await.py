
def is_await(ann) -> bool:
    if ann is _Await:
        return True
    return get_origin(ann) is _Await

