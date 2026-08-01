
def has_uninhabited_component(t: Type | None) -> bool:
    return t is not None and t.accept(HasUninhabitedComponentsQuery())

