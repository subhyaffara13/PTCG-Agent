
def register_decomposition_for_jvp(fn):
    return register_decomposition(fn, registry=decomposition_table_for_jvp)

