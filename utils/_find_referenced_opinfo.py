
def _find_referenced_opinfo(referenced_name, variant_name, *, op_db=None):
    """
    Finds the OpInfo with the given name that has no variant name.
    """
    # NOTE: searching the global op_db doesn't work when OpInfos are split into
    # different modules, as otherwise the op_db will not be fully constructed
    # yet. So, instead the local op_db must be passed in explicitly.
    if op_db is None:
        from torch.testing._internal.common_methods_invocations import op_db

    for opinfo in op_db:
        if opinfo.name == referenced_name and opinfo.variant_test_name == variant_name:
            return opinfo

