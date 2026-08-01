
def common_constants() -> set[int]:
    return {
        # We zero-one specialize shapes, so specialize these constants
        # too
        0,
        1,
    }

