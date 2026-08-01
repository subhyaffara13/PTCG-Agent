
def _add_method_by_spec(
    api: SemanticAnalyzerPluginInterface | CheckerPluginInterface,
    info: TypeInfo,
    name: str,
    spec: MethodSpec,
    *,
    is_classmethod: bool,
    is_staticmethod: bool,
) -> tuple[FuncDef | Decorator, SymbolTableNode]:
    args, return_type, self_type, tvar_defs = spec

    assert not (
        is_classmethod is True and is_staticmethod is True
    ), "Can't add a new method that's both staticmethod and classmethod."

    if isinstance(api, SemanticAnalyzerPluginInterface):
        function_type = api.named_type("builtins.function")
    else:
        function_type = api.named_generic_type("builtins.function", [])

    if is_classmethod:
        self_type = self_type or TypeType(fill_typevars(info))
        first = [Argument(Var("_cls"), self_type, None, ARG_POS, True)]
    elif is_staticmethod:
        first = []
    else:
        self_type = self_type or fill_typevars(info)
        first = [Argument(Var("self"), self_type, None, ARG_POS)]
    args = first + args

    arg_types, arg_names, arg_kinds = [], [], []
    for arg in args:
        assert arg.type_annotation, "All arguments must be fully typed."
        arg_types.append(arg.type_annotation)
        arg_names.append(arg.variable.name)
        arg_kinds.append(arg.kind)

    signature = CallableType(arg_types, arg_kinds, arg_names, return_type, function_type)
    if tvar_defs:
        signature.variables = tuple(tvar_defs)

    func = FuncDef(name, args, Block([PassStmt()]))
    func.info = info
    func.type = set_callable_name(signature, func)
    func.is_class = is_classmethod
    func.is_static = is_staticmethod
    func._fullname = info.fullname + "." + name
    func.line = info.line

    # Add decorator for is_staticmethod. It's unnecessary for is_classmethod.
    if is_staticmethod:
        func.is_decorated = True
        v = Var(name, func.type)
        v.info = info
        v._fullname = func._fullname
        v.is_staticmethod = True
        dec = Decorator(func, [], v)
        dec.line = info.line
        sym = SymbolTableNode(MDEF, dec)
        sym.plugin_generated = True
        return dec, sym

    sym = SymbolTableNode(MDEF, func)
    sym.plugin_generated = True
    return func, sym

