from typing import List, Optional

def add_method(
    api: SemanticAnalyzerPluginInterface | CheckerPluginInterface,
    cls: ClassDef,
    name: str,
    args: list[Argument],
    return_type: Type,
    self_type: Type | None = None,
    tvar_def: TypeVarType | None = None,
    is_classmethod: bool = False,
) -> None:
    """Very closely related to `mypy.plugins.common.add_method_to_class`, with a few pydantic-specific changes."""
    info = cls.info

    # First remove any previously generated methods with the same name
    # to avoid clashes and problems in the semantic analyzer.
    if name in info.names:
        sym = info.names[name]
        if sym.plugin_generated and isinstance(sym.node, FuncDef):
            cls.defs.body.remove(sym.node)  # pragma: no cover

    if isinstance(api, SemanticAnalyzerPluginInterface):
        function_type = api.named_type('builtins.function')
    else:
        function_type = api.named_generic_type('builtins.function', [])

    if is_classmethod:
        self_type = self_type or TypeType(fill_typevars(info))
        first = [Argument(Var('_cls'), self_type, None, ARG_POS, True)]
    else:
        self_type = self_type or fill_typevars(info)
        # `self` is positional *ONLY* here, but this can't be expressed
        # fully in the mypy internal API. ARG_POS is the closest we can get.
        # Using ARG_POS will, however, give mypy errors if a `self` field
        # is present on a model:
        #
        #     Name "self" already defined (possibly by an import)  [no-redef]
        #
        # As a workaround, we give this argument a name that will
        # never conflict. By its positional nature, this name will not
        # be used or exposed to users.
        first = [Argument(Var('__pydantic_self__'), self_type, None, ARG_POS)]
    args = first + args

    arg_types, arg_names, arg_kinds = [], [], []
    for arg in args:
        assert arg.type_annotation, 'All arguments must be fully typed.'
        arg_types.append(arg.type_annotation)
        arg_names.append(arg.variable.name)
        arg_kinds.append(arg.kind)

    signature = CallableType(
        arg_types, arg_kinds, arg_names, return_type, function_type, variables=[tvar_def] if tvar_def else None
    )

    func = FuncDef(name, args, Block([PassStmt()]))
    func.info = info
    func.type = set_callable_name(signature, func)
    func.is_class = is_classmethod
    func._fullname = info.fullname + '.' + name
    func.line = info.line

    # NOTE: we would like the plugin generated node to dominate, but we still
    # need to keep any existing definitions so they get semantically analyzed.
    if name in info.names:
        # Get a nice unique name instead.
        r_name = get_unique_redefinition_name(name, info.names)
        info.names[r_name] = info.names[name]

    # Add decorator for is_classmethod
    # The dataclasses plugin claims this is unnecessary for classmethods, but not including it results in a
    # signature incompatible with the superclass, which causes mypy errors to occur for every subclass of BaseModel.
    if is_classmethod:
        func.is_decorated = True
        v = Var(name, func.type)
        v.info = info
        v._fullname = func._fullname
        v.is_classmethod = True
        dec = Decorator(func, [NameExpr('classmethod')], v)
        dec.line = info.line
        sym = SymbolTableNode(MDEF, dec)
    else:
        sym = SymbolTableNode(MDEF, func)
    sym.plugin_generated = True
    info.names[name] = sym

    info.defn.defs.body.append(func)


def add_method(
    ctx: ClassDefContext,
    name: str,
    args: List[Argument],
    return_type: Type,
    self_type: Optional[Type] = None,
    tvar_def: Optional[TypeVarDef] = None,
    is_classmethod: bool = False,
    is_new: bool = False,
    # is_staticmethod: bool = False,
) -> None:
    """
    Adds a new method to a class.

    This can be dropped if/when https://github.com/python/mypy/issues/7301 is merged
    """
    info = ctx.cls.info

    # First remove any previously generated methods with the same name
    # to avoid clashes and problems in the semantic analyzer.
    if name in info.names:
        sym = info.names[name]
        if sym.plugin_generated and isinstance(sym.node, FuncDef):
            ctx.cls.defs.body.remove(sym.node)  # pragma: no cover

    self_type = self_type or fill_typevars(info)
    if is_classmethod or is_new:
        first = [Argument(Var('_cls'), TypeType.make_normalized(self_type), None, ARG_POS)]
    # elif is_staticmethod:
    #     first = []
    else:
        self_type = self_type or fill_typevars(info)
        first = [Argument(Var('__pydantic_self__'), self_type, None, ARG_POS)]
    args = first + args
    arg_types, arg_names, arg_kinds = [], [], []
    for arg in args:
        assert arg.type_annotation, 'All arguments must be fully typed.'
        arg_types.append(arg.type_annotation)
        arg_names.append(get_name(arg.variable))
        arg_kinds.append(arg.kind)

    function_type = ctx.api.named_type(f'{BUILTINS_NAME}.function')
    signature = CallableType(
        arg_types, arg_kinds, arg_names, return_type, function_type, variables=[tvar_def] if tvar_def else None
    )

    func = FuncDef(name, args, Block([PassStmt()]))
    func.info = info
    func.type = set_callable_name(signature, func)
    func.is_class = is_classmethod
    # func.is_static = is_staticmethod
    func._fullname = get_fullname(info) + '.' + name
    func.line = info.line

    # NOTE: we would like the plugin generated node to dominate, but we still
    # need to keep any existing definitions so they get semantically analyzed.
    if name in info.names:
        # Get a nice unique name instead.
        r_name = get_unique_redefinition_name(name, info.names)
        info.names[r_name] = info.names[name]

    if is_classmethod:  # or is_staticmethod:
        func.is_decorated = True
        v = Var(name, func.type)
        v.info = info
        v._fullname = func._fullname
        # if is_classmethod:
        v.is_classmethod = True
        dec = Decorator(func, [NameExpr('classmethod')], v)
        # else:
        #     v.is_staticmethod = True
        #     dec = Decorator(func, [NameExpr('staticmethod')], v)

        dec.line = info.line
        sym = SymbolTableNode(MDEF, dec)
    else:
        sym = SymbolTableNode(MDEF, func)
    sym.plugin_generated = True

    info.names[name] = sym
    info.defn.defs.body.append(func)


def add_method(
    ctx: ClassDefContext,
    name: str,
    args: list[Argument],
    return_type: Type,
    self_type: Type | None = None,
    tvar_def: TypeVarType | None = None,
    is_classmethod: bool = False,
    is_staticmethod: bool = False,
) -> None:
    """
    Adds a new method to a class.
    Deprecated, use add_method_to_class() instead.
    """
    add_method_to_class(
        ctx.api,
        ctx.cls,
        name=name,
        args=args,
        return_type=return_type,
        self_type=self_type,
        tvar_def=tvar_def,
        is_classmethod=is_classmethod,
        is_staticmethod=is_staticmethod,
    )


def add_method(*clazzes, **kwargs):
    """Returns a decorator function that adds a new method to one or
    more classes."""
    allowDefault = kwargs.get("allowDefaultTable", False)

    def wrapper(method):
        done = []
        for clazz in clazzes:
            if clazz in done:
                continue  # Support multiple names of a clazz
            done.append(clazz)
            assert allowDefault or clazz != DefaultTable, "Oops, table class not found."
            assert (
                method.__name__ not in clazz.__dict__
            ), "Oops, class '%s' has method '%s'." % (clazz.__name__, method.__name__)
            setattr(clazz, method.__name__, method)
        return None

    return wrapper

