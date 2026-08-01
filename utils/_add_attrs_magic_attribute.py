
def _add_attrs_magic_attribute(
    ctx: mypy.plugin.ClassDefContext, attrs: list[tuple[str, Type | None]]
) -> None:
    any_type = AnyType(TypeOfAny.explicit)
    attributes_types: list[Type] = [
        ctx.api.named_type_or_none("attr.Attribute", [attr_type or any_type]) or any_type
        for _, attr_type in attrs
    ]
    fallback_type = ctx.api.named_type(
        "builtins.tuple", [ctx.api.named_type_or_none("attr.Attribute", [any_type]) or any_type]
    )

    attr_name = MAGIC_ATTR_CLS_NAME_TEMPLATE.format(ctx.cls.fullname.replace(".", "_"))
    ti = ctx.api.basic_new_typeinfo(attr_name, fallback_type, 0)
    for (name, _), attr_type in zip(attrs, attributes_types):
        var = Var(name, attr_type)
        var._fullname = name
        var.is_property = True
        proper_type = get_proper_type(attr_type)
        if isinstance(proper_type, Instance):
            var.info = proper_type.type
        ti.names[name] = SymbolTableNode(MDEF, var, plugin_generated=True)
    attributes_type = Instance(ti, [])

    # We need to stash the type of the magic attribute so it can be
    # loaded on cached runs.
    ctx.cls.info.names[attr_name] = SymbolTableNode(MDEF, ti, plugin_generated=True)

    add_attribute_to_class(
        ctx.api,
        ctx.cls,
        MAGIC_ATTR_NAME,
        TupleType(attributes_types, fallback=attributes_type),
        fullname=f"{ctx.cls.fullname}.{MAGIC_ATTR_NAME}",
        override_allow_incompatible=True,
        is_classvar=True,
    )

