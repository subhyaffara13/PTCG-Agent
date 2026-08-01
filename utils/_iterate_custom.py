
def _iterate_custom(space, items):
    raise CustomSpaceError(
        f"Unable to iterate over {items}, since {space} "
        "is a custom `gym.Space` instance (i.e. not one of "
        "`Box`, `Dict`, etc...)."
    )

