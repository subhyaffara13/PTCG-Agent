
def is_imprecise(t: Type) -> bool:
    return t.accept(HasAnyQuery())

