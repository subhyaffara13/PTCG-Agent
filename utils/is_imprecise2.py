
def is_imprecise2(t: Type) -> bool:
    return t.accept(HasAnyQuery2())

