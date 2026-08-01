
def has_erased_component(t: Type | None) -> bool:
    return t is not None and t.accept(HasErasedComponentsQuery())

