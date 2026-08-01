
def mirror_rel_op(type: type) -> type[sympy.Rel] | None:
    return _MIRROR_REL_OP.get(type)

