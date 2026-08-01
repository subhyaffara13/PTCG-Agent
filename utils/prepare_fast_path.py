
def prepare_fast_path(
    ir: ClassIR,
    module_name: str,
    cdef: ClassDef,
    mapper: Mapper,
    node: SymbolNode | None,
    options: CompilerOptions,
) -> None:
    """Add fast (direct) variants of methods in non-extension classes."""
    if ir.is_enum:
        # We check that non-empty enums are implicitly final in mypy, so we
        # can generate direct calls to enum methods.
        if isinstance(node, OverloadedFuncDef):
            if node.is_property:
                return
            node = node.impl
        if not isinstance(node, FuncDef):
            # TODO: support decorated methods (at least @classmethod and @staticmethod).
            return
        # The simplest case is a regular or overloaded method without decorators. In this
        # case we can generate practically identical IR method body, but with a signature
        # suitable for direct calls (usual non-extension class methods are converted to
        # callable classes, and thus have an extra __mypyc_self__ argument).
        name = FAST_PREFIX + node.name
        sig = mapper.fdef_to_sig(node, options.strict_dunders_typing)
        decl = FuncDecl(name, cdef.name, module_name, sig, FUNC_NORMAL)
        ir.method_decls[name] = decl
    return

