
def is_c_py_ssize_t_rprimitive(rtype: RType) -> TypeGuard[RPrimitive]:
    return rtype is c_pyssize_t_rprimitive

