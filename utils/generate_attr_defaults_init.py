
def generate_attr_defaults_init(
    builder: IRBuilder, cdef: ClassDef, default_assignments: list[tuple[AssignmentStmt, str]]
) -> None:
    """Generate an initialization method for default attr values (from class vars).

    Under separate compilation, the emitted __mypyc_defaults_setup chains to
    the nearest ancestor that has the method (Python __init__ style), then
    sets only this class's own defaults; inherited defaults are produced by
    the chain at runtime. The ancestor lookup uses cls.mro[1:] and relies on
    prepare.py having registered the FuncDecl on every class that needs one
    before any IR build runs. IR build within a compilation group proceeds
    in filename order, so this class may be IR-built before its base, and a
    method_decls lookup that depended on the base having been IR-built first
    would miss. Without separate compilation, find_attr_initializers has
    already collected the full MRO's defaults into default_assignments, so
    we inline them all as before.
    """
    cls = builder.mapper.type_to_ir[cdef.info]
    if cls.builtin_base:
        return

    parent_with_defaults: ClassIR | None = None
    if builder.options.separate:
        for ancestor in cls.mro[1:]:
            if MYPYC_DEFAULTS_SETUP in ancestor.method_decls:
                parent_with_defaults = ancestor
                break

    if not default_assignments and parent_with_defaults is None:
        return

    with builder.enter_method(cls, MYPYC_DEFAULTS_SETUP, bool_rprimitive):
        self_var = builder.self()

        # Chain to parent's setup so inherited defaults run first; propagate
        # its False return so a parent default that raised still aborts
        # instance creation rather than being silently swallowed here.
        if parent_with_defaults is not None:
            decl = parent_with_defaults.method_decl(MYPYC_DEFAULTS_SETUP)
            parent_ok = builder.builder.call(decl, [self_var], [ARG_POS], [None], cdef.line)
            fail_block, continue_block = BasicBlock(), BasicBlock()
            builder.add(Branch(parent_ok, continue_block, fail_block, Branch.BOOL))
            builder.activate_block(fail_block)
            builder.add(Return(builder.false()))
            builder.activate_block(continue_block)

        for stmt, origin_module in default_assignments:
            lvalue = stmt.lvalues[0]
            assert isinstance(lvalue, NameExpr), lvalue
            if not stmt.is_final_def and not is_constant(stmt.rvalue):
                builder.warning("Unsupported default attribute value", stmt.rvalue.line)

            attr_type = cls.attr_type(lvalue.name)
            # When the default comes from a parent in a different module,
            # set the globals lookup module so NameExpr references resolve
            # against the correct module's globals dict.
            builder.globals_lookup_module = (
                origin_module if origin_module != builder.module_name else None
            )
            try:
                val = builder.coerce(builder.accept(stmt.rvalue), attr_type, stmt.line)
            finally:
                builder.globals_lookup_module = None
            init = SetAttr(self_var, lvalue.name, val, stmt.rvalue.line)
            init.mark_as_initializer()
            builder.add(init)

        builder.add(Return(builder.true()))

