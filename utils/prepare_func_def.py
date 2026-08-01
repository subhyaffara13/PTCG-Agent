
def prepare_func_def(
    module_name: str,
    class_name: str | None,
    fdef: FuncDef,
    mapper: Mapper,
    options: CompilerOptions,
) -> FuncDecl:
    kind = (
        FUNC_CLASSMETHOD
        if fdef.is_class
        else (FUNC_STATICMETHOD if fdef.is_static else FUNC_NORMAL)
    )
    sig = mapper.fdef_to_sig(fdef, options.strict_dunders_typing)
    decl = FuncDecl(
        fdef.name,
        class_name,
        module_name,
        sig,
        kind,
        is_generator=fdef.is_generator,
        is_coroutine=fdef.is_coroutine,
    )
    mapper.func_to_decl[fdef] = decl
    return decl

