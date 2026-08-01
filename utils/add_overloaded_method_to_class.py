
def add_overloaded_method_to_class(
    api: SemanticAnalyzerPluginInterface | CheckerPluginInterface,
    cls: ClassDef,
    name: str,
    items: list[MethodSpec],
    is_classmethod: bool = False,
    is_staticmethod: bool = False,
) -> OverloadedFuncDef:
    """Adds a new overloaded method to a class definition."""
    assert len(items) >= 2, "Overloads must contain at least two cases"

    # Save old definition, if it exists.
    _prepare_class_namespace(cls, name)

    # Create function bodies for each passed method spec.
    funcs: list[Decorator | FuncDef] = []
    for item in items:
        func, _sym = _add_method_by_spec(
            api,
            cls.info,
            name=name,
            spec=item,
            is_classmethod=is_classmethod,
            is_staticmethod=is_staticmethod,
        )
        if isinstance(func, FuncDef):
            var = Var(func.name, func.type)
            var.set_line(func.line)
            func.is_decorated = True

            deco = Decorator(func, [], var)
        else:
            deco = func
        deco.is_overload = True
        funcs.append(deco)

    # Create the final OverloadedFuncDef node:
    overload_def = OverloadedFuncDef(funcs)
    overload_def.info = cls.info
    overload_def.is_class = is_classmethod
    overload_def.is_static = is_staticmethod
    sym = SymbolTableNode(MDEF, overload_def)
    sym.plugin_generated = True

    cls.info.names[name] = sym
    cls.info.defn.defs.body.append(overload_def)
    return overload_def

