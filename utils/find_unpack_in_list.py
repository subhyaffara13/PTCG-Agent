
def find_unpack_in_list(items: Sequence[Type]) -> int | None:
    unpack_index: int | None = None
    for i, item in enumerate(items):
        if isinstance(item, UnpackType):
            # We cannot fail here, so we must check this in an earlier
            # semanal phase.
            # Funky code here avoids mypyc narrowing the type of unpack_index.
            old_index = unpack_index
            assert old_index is None
            # Don't return so that we can also sanity-check there is only one.
            unpack_index = i
    return unpack_index

