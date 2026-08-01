
def build_tensor_from_id(data: int | object) -> int | None:
    if isinstance(data, int):
        # just the id, can't really do anything
        return data
    return None

