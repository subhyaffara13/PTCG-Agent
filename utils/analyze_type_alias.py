
def analyze_type_alias(
    type: Type,
    api: SemanticAnalyzerCoreInterface,
    tvar_scope: TypeVarLikeScope,
    plugin: Plugin,
    options: Options,
    cur_mod_node: MypyFile,
    is_typeshed_stub: bool,
    allow_placeholder: bool = False,
    in_dynamic_func: bool = False,
    global_scope: bool = True,
    allowed_alias_tvars: list[TypeVarLikeType] | None = None,
    erase_tvar_defs: list[TypeVarType] | None = None,
    alias_type_params_names: list[str] | None = None,
    python_3_12_type_alias: bool = False,
) -> tuple[Type, set[str]]:
    """Analyze r.h.s. of a (potential) type alias definition.

    If `node` is valid as a type alias rvalue, return the resulting type and a set of
    full names of type aliases it depends on (directly or indirectly).
    'node' must have been semantically analyzed.
    """
    analyzer = TypeAnalyser(
        api,
        tvar_scope,
        plugin,
        options,
        cur_mod_node,
        is_typeshed_stub,
        defining_alias=True,
        allow_placeholder=allow_placeholder,
        prohibit_self_type="type alias target",
        allowed_alias_tvars=allowed_alias_tvars,
        erase_tvar_defs=erase_tvar_defs,
        alias_type_params_names=alias_type_params_names,
        python_3_12_type_alias=python_3_12_type_alias,
    )
    analyzer.in_dynamic_func = in_dynamic_func
    analyzer.global_scope = global_scope
    res = analyzer.anal_type(type, nested=False)
    return res, analyzer.aliases_used

