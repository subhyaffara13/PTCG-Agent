
def prepare_method_def(
    ir: ClassIR,
    module_name: str,
    cdef: ClassDef,
    mapper: Mapper,
    node: FuncDef | Decorator,
    options: CompilerOptions,
) -> None:
    if isinstance(node, FuncDef):
        ir.method_decls[node.name] = prepare_func_def(
            module_name, cdef.name, node, mapper, options
        )
    elif isinstance(node, Decorator):
        # TODO: do something about abstract methods here. Currently, they are handled just like
        # normal methods.
        decl = prepare_func_def(module_name, cdef.name, node.func, mapper, options)
        if not node.decorators:
            ir.method_decls[node.name] = decl
        elif isinstance(node.decorators[0], MemberExpr) and node.decorators[0].name == "setter":
            # Make property setter name different than getter name so there are no
            # name clashes when generating C code, and property lookup at the IR level
            # works correctly.
            decl.name = PROPSET_PREFIX + decl.name
            decl.is_prop_setter = True
            # Making the argument implicitly positional-only avoids unnecessary glue methods
            decl.sig.args[1].pos_only = True
            ir.method_decls[PROPSET_PREFIX + node.name] = decl

        if node.func.is_property:
            assert node.func.type, f"Expected return type annotation for property '{node.name}'"
            decl.is_prop_getter = True
            ir.property_types[node.name] = decl.sig.ret_type

