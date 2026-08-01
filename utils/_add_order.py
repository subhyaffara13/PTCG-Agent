
def _add_order(ctx: mypy.plugin.ClassDefContext, adder: MethodAdder) -> None:
    """Generate all the ordering methods for this class."""
    bool_type = ctx.api.named_type("builtins.bool")
    object_type = ctx.api.named_type("builtins.object")
    # Make the types be:
    #    AT = TypeVar('AT')
    #    def __lt__(self: AT, other: AT) -> bool
    # This way comparisons with subclasses will work correctly.
    fullname = f"{ctx.cls.info.fullname}.{SELF_TVAR_NAME}"
    tvd = TypeVarType(
        SELF_TVAR_NAME,
        fullname,
        # Namespace is patched per-method below.
        id=TypeVarId(-1, namespace=""),
        values=[],
        upper_bound=object_type,
        default=AnyType(TypeOfAny.from_omitted_generics),
    )
    self_tvar_expr = TypeVarExpr(
        SELF_TVAR_NAME, fullname, [], object_type, AnyType(TypeOfAny.from_omitted_generics)
    )
    ctx.cls.info.names[SELF_TVAR_NAME] = SymbolTableNode(MDEF, self_tvar_expr)

    for method in ["__lt__", "__le__", "__gt__", "__ge__"]:
        namespace = f"{ctx.cls.info.fullname}.{method}"
        tvd = tvd.copy_modified(id=TypeVarId(tvd.id.raw_id, namespace=namespace))
        args = [Argument(Var("other", tvd), tvd, None, ARG_POS)]
        adder.add_method(method, args, bool_type, self_type=tvd, tvd=tvd)

