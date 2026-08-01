
def generate_assert(check: bool) -> bool:
    return (check or config.debug_index_asserts) and config.assert_indirect_indexing

