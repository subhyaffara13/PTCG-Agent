
def _warn_for_non_extern_non_static_global_variable(decl):
    if not decl.storage:
        import warnings
        warnings.warn("Global variable '%s' in cdef(): for consistency "
                      "with C it should have a storage class specifier "
                      "(usually 'extern')" % (decl.name,))

