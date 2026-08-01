
def transform_class_def(builder: IRBuilder, cdef: ClassDef) -> None:
    """Create IR for a class definition.

    This can generate both extension (native) and non-extension
    classes.  These are generated in very different ways. In the
    latter case we construct a Python type object at runtime by doing
    the equivalent of "type(name, bases, dict)" in IR. Extension
    classes are defined via C structs that are generated later in
    mypyc.codegen.emitclass.

    This is the main entry point to this module.
    """
    if cdef.info not in builder.mapper.type_to_ir:
        builder.error("Nested class definitions not supported", cdef.line)
        return

    ir = builder.mapper.type_to_ir[cdef.info]

    # We do this check here because the base field of parent
    # classes aren't necessarily populated yet at
    # prepare_class_def time.
    if any(ir.base_mro[i].base != ir.base_mro[i + 1] for i in range(len(ir.base_mro) - 1)):
        builder.error("Multiple inheritance is not supported (except for traits)", cdef.line)

    if ir.allow_interpreted_subclasses:
        for parent in ir.mro:
            if not parent.allow_interpreted_subclasses:
                builder.error(
                    'Base class "{}" does not allow interpreted subclasses'.format(
                        parent.fullname
                    ),
                    cdef.line,
                )

    # Currently, we only create non-extension classes for classes that are
    # decorated or inherit from Enum. Classes decorated with @trait do not
    # apply here, and are handled in a different way.
    if ir.is_ext_class:
        cls_type = dataclass_type(cdef)
        if cls_type is None:
            cls_builder: ClassBuilder = ExtClassBuilder(builder, cdef)
        elif cls_type in ["dataclasses", "attr-auto"]:
            cls_builder = DataClassBuilder(builder, cdef)
        elif cls_type == "attr":
            cls_builder = AttrsClassBuilder(builder, cdef)
        else:
            raise ValueError(cls_type)
    else:
        cls_builder = NonExtClassBuilder(builder, cdef)

    # Set up class body context so that intra-class ClassVar references
    # (e.g. C = A | B where A is defined earlier in the same class) can be
    # resolved from the class being built instead of module globals.
    builder.class_body_classvars = {}
    builder.class_body_obj = cls_builder.class_body_obj()
    builder.class_body_ir = ir

    for stmt in cdef.defs.body:
        if (
            isinstance(stmt, (FuncDef, Decorator, OverloadedFuncDef))
            and stmt.name == GENERATOR_HELPER_NAME
        ):
            builder.error(
                f'Method name "{stmt.name}" is reserved for mypyc internal use', stmt.line
            )

        if isinstance(stmt, OverloadedFuncDef) and stmt.is_property:
            if isinstance(cls_builder, NonExtClassBuilder):
                # properties with both getters and setters in non_extension
                # classes not supported
                builder.error("Property setters not supported in non-extension classes", stmt.line)
            for item in stmt.items:
                with builder.catch_errors(stmt.line):
                    cls_builder.add_method(get_func_def(item))
        elif isinstance(stmt, (FuncDef, Decorator, OverloadedFuncDef)):
            # Ignore plugin generated methods (since they have no
            # bodies to compile and will need to have the bodies
            # provided by some other mechanism.)
            if cdef.info.names[stmt.name].plugin_generated:
                continue
            with builder.catch_errors(stmt.line):
                cls_builder.add_method(get_func_def(stmt))
        elif isinstance(stmt, PassStmt) or (
            isinstance(stmt, ExpressionStmt) and isinstance(stmt.expr, EllipsisExpr)
        ):
            continue
        elif isinstance(stmt, AssignmentStmt):
            if len(stmt.lvalues) != 1:
                builder.error("Multiple assignment in class bodies not supported", stmt.line)
                continue
            lvalue = stmt.lvalues[0]
            if not isinstance(lvalue, NameExpr):
                builder.error(
                    "Only assignment to variables is supported in class bodies", stmt.line
                )
                continue
            # We want to collect class variables in a dictionary for both real
            # non-extension classes and fake dataclass ones.
            cls_builder.add_attr(lvalue, stmt)
            # Track this ClassVar so subsequent class body statements can reference it.
            if is_class_var(lvalue) or stmt.is_final_def:
                assert isinstance(lvalue.node, Var), lvalue.node
                builder.class_body_classvars[lvalue.node] = None

        elif isinstance(stmt, ExpressionStmt) and isinstance(stmt.expr, StrExpr):
            # Docstring. Ignore
            pass
        else:
            builder.error("Unsupported statement in class body", stmt.line)

    # Clear class body context (nested classes are rejected above, so no need to save/restore).
    builder.class_body_classvars = {}
    builder.class_body_obj = None
    builder.class_body_ir = None

    # Generate implicit property setters/getters
    for name, decl in ir.method_decls.items():
        if decl.implicit and decl.is_prop_getter:
            getter_ir = gen_property_getter_ir(builder, decl, cdef, ir.is_trait)
            builder.functions.append(getter_ir)
            ir.methods[getter_ir.decl.name] = getter_ir

            setter_ir = None
            setter_name = PROPSET_PREFIX + name
            if setter_name in ir.method_decls:
                setter_ir = gen_property_setter_ir(
                    builder, ir.method_decls[setter_name], cdef, ir.is_trait
                )
                builder.functions.append(setter_ir)
                ir.methods[setter_name] = setter_ir

            ir.properties[name] = (getter_ir, setter_ir)
            # TODO: Generate glue method if needed?
            # TODO: Do we need interpreted glue methods? Maybe not?

    cls_builder.finalize(ir)

