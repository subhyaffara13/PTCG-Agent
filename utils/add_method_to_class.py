
def add_method_to_class(
    api: SemanticAnalyzerPluginInterface | CheckerPluginInterface,
    cls: ClassDef,
    name: str,
    # MethodSpec items kept for backward compatibility:
    args: list[Argument],
    return_type: Type,
    self_type: Type | None = None,
    tvar_def: list[TypeVarType] | TypeVarType | None = None,
    is_classmethod: bool = False,
    is_staticmethod: bool = False,
) -> FuncDef | Decorator:
    """Adds a new method to a class definition."""
    _prepare_class_namespace(cls, name)

    if tvar_def is not None and not isinstance(tvar_def, list):
        tvar_def = [tvar_def]

    func, sym = _add_method_by_spec(
        api,
        cls.info,
        name,
        MethodSpec(args=args, return_type=return_type, self_type=self_type, tvar_defs=tvar_def),
        is_classmethod=is_classmethod,
        is_staticmethod=is_staticmethod,
    )
    cls.info.names[name] = sym
    cls.info.defn.defs.body.append(func)
    return func

