
def is_future(ann) -> bool:
    if ann is Future:
        raise RuntimeError(
            "Attempted to use Future without a "
            "contained type. Please add a contained type, e.g. "
            "Future[int]"
        )
    return get_origin(ann) is Future

