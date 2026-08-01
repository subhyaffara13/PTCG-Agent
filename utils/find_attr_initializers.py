
def find_attr_initializers(
    builder: IRBuilder, cdef: ClassDef
) -> tuple[set[str], list[tuple[AssignmentStmt, str]]]:
    """Find initializers of attributes in a class body.

    Under separate compilation, only this class's own body is walked, and
    generate_attr_defaults_init emits a runtime call to the parent's
    __mypyc_defaults_setup so inherited defaults are produced by chaining,
    not by inlining. Walking the MRO here would break under separate=True
    with mypy's incremental cache: a base class loaded from the cache has
    an empty ClassDef.defs.body (mypy/nodes.py::ClassDef.serialize doesn't
    serialize the class body), so inherited assignments would be silently
    dropped and the subclass's __mypyc_defaults_setup would leave inherited
    slots in the "undefined" state at runtime.

    Without separate compilation, all modules are parsed in the same pass
    and the MRO walk is safe; we keep the original inline-all behavior
    there as an optimization (no chain call needed for instance creation).
    """
    cls = builder.mapper.type_to_ir[cdef.info]
    if cls.builtin_base:
        return set(), []

    cls_type = dataclass_type(cdef)
    attrs_with_defaults: set[str] = set()
    default_assignments: list[tuple[AssignmentStmt, str]] = []

    # TODO: Support nested statements
    if builder.options.separate:
        infos: list[TypeInfo] = [cdef.info]
    else:
        infos = list(reversed(cdef.info.mro))

    for info in infos:
        info_ir = builder.mapper.type_to_ir.get(info)
        if info_ir is None:
            continue
        for stmt in info.defn.defs.body:
            if not isinstance(stmt, AssignmentStmt):
                continue
            name = default_attr_name(stmt, info_ir, cls_type)
            if name is None:
                continue
            attrs_with_defaults.add(name)
            default_assignments.append((stmt, info.module_name))

    return attrs_with_defaults, default_assignments

