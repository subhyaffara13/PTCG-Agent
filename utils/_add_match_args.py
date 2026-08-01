
def _add_match_args(ctx: mypy.plugin.ClassDefContext, attributes: list[Attribute]) -> None:
    if (
        "__match_args__" not in ctx.cls.info.names
        or ctx.cls.info.names["__match_args__"].plugin_generated
    ):
        str_type = ctx.api.named_type("builtins.str")
        match_args = TupleType(
            [
                str_type.copy_modified(last_known_value=LiteralType(attr.name, fallback=str_type))
                for attr in attributes
                if not attr.kw_only and attr.init
            ],
            fallback=ctx.api.named_type("builtins.tuple"),
        )
        add_attribute_to_class(api=ctx.api, cls=ctx.cls, name="__match_args__", typ=match_args)

