
def find_singledispatch_register_impls(
    modules: list[MypyFile], errors: Errors
) -> SingledispatchInfo:
    visitor = SingledispatchVisitor(errors)
    for module in modules:
        visitor.current_path = module.path
        module.accept(visitor)
    return SingledispatchInfo(visitor.singledispatch_impls, visitor.decorators_to_remove)

