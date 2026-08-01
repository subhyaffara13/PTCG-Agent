
def deserialize_and_fixup_type(data: str | JsonDict, api: SemanticAnalyzerPluginInterface) -> Type:
    typ = deserialize_type(data)
    assert modules_state.node_fixer is not None
    typ.accept(modules_state.node_fixer.type_fixer)
    return typ

