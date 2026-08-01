
def freshen_all_functions_type_vars(t: T) -> T:
    result: Type
    has_generic_callable.reset()
    if not t.accept(has_generic_callable):
        return t  # Fast path to avoid expensive freshening
    else:
        result = t.accept(FreshenCallableVisitor())
        assert isinstance(result, type(t))
        return result

