
def get_native_impl_ids(builder: IRBuilder, singledispatch_func: FuncDef) -> dict[FuncDef, int]:
    """Return a dict of registered implementation to native implementation ID for all
    implementations
    """
    impls = builder.singledispatch_impls[singledispatch_func]
    return {impl: i for i, (typ, impl) in enumerate(impls) if not is_decorated(builder, impl)}

