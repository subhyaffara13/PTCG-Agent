
def _attribute_from_attrib_maker(
    ctx: mypy.plugin.ClassDefContext,
    auto_attribs: bool,
    class_kw_only: bool,
    lhs: NameExpr,
    rvalue: CallExpr,
    stmt: AssignmentStmt,
) -> Attribute | None:
    """Return an Attribute from the assignment or None if you can't make one."""
    if auto_attribs and not stmt.new_syntax:
        # auto_attribs requires an annotation on *every* attr.ib.
        assert lhs.node is not None
        ctx.api.msg.need_annotation_for_var(lhs.node, stmt)
        return None

    if len(stmt.lvalues) > 1:
        ctx.api.fail("Too many names for one attribute", stmt)
        return None

    # This is the type that belongs in the __init__ method for this attrib.
    init_type = stmt.type

    # Read all the arguments from the call.
    init = _get_bool_argument(ctx, rvalue, "init", True)
    # The class decorator kw_only value can be overridden by the attribute value
    # See https://github.com/python-attrs/attrs/pull/1457
    kw_only = _get_bool_argument(ctx, rvalue, "kw_only", class_kw_only)

    # TODO: Check for attr.NOTHING
    attr_has_default = bool(_get_argument(rvalue, "default"))
    attr_has_factory = bool(_get_argument(rvalue, "factory"))

    if attr_has_default and attr_has_factory:
        ctx.api.fail('Can\'t pass both "default" and "factory".', rvalue)
    elif attr_has_factory:
        attr_has_default = True

    # If the type isn't set through annotation but is passed through `type=` use that.
    type_arg = _get_argument(rvalue, "type")
    if type_arg and not init_type:
        try:
            un_type = expr_to_unanalyzed_type(type_arg, ctx.api.options, ctx.api.is_stub_file)
        except TypeTranslationError:
            ctx.api.fail("Invalid argument to type", type_arg)
        else:
            init_type = ctx.api.anal_type(un_type)
            if init_type and isinstance(lhs.node, Var) and not lhs.node.type:
                # If there is no annotation, add one.
                lhs.node.type = init_type
                lhs.is_inferred_def = False

    # Note: convert is deprecated but works the same as converter.
    converter = _get_argument(rvalue, "converter")
    convert = _get_argument(rvalue, "convert")
    if convert and converter:
        ctx.api.fail('Can\'t pass both "convert" and "converter".', rvalue)
    elif convert:
        ctx.api.fail("convert is deprecated, use converter", rvalue)
        converter = convert
    converter_info = _parse_converter(ctx, converter)

    # Custom alias might be defined:
    alias = None
    alias_expr = _get_argument(rvalue, "alias")
    if alias_expr:
        alias = ctx.api.parse_str_literal(alias_expr)
        if alias is None:
            ctx.api.fail(
                '"alias" argument to attrs field must be a string literal',
                rvalue,
                code=LITERAL_REQ,
            )
    name = unmangle(lhs.name)
    return Attribute(
        name, alias, ctx.cls.info, attr_has_default, init, kw_only, converter_info, stmt, init_type
    )

