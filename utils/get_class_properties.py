
def get_class_properties(cls, self_name):
    """
    Get a list of Property objects representing the properties of a class.

    Args:
        cls:  The class to get properties of.
        self_name: The name of the class that the properties should belong to.
    Returns:
        A list of Property objects corresponding to the properties of cls. Property
        here refers to the subclass of TreeView.
    """
    props = inspect.getmembers(cls, predicate=lambda m: isinstance(m, property))
    # Any property that should not compiled must be in this list on the Module.
    unused_properties = getattr(cls, "__jit_unused_properties__", [])

    # Create Property TreeView objects from inspected property objects.
    properties = []
    for prop in props:
        if prop[0] not in unused_properties and not should_drop(prop[1].fget):
            getter = get_jit_def(
                prop[1].fget, f"__{prop[0]}_getter", self_name=self_name
            )
            setter = (
                get_jit_def(prop[1].fset, f"__{prop[0]}_setter", self_name=self_name)
                if prop[1].fset
                else None
            )
            properties.append(
                Property(getter.range(), Ident(getter.range(), prop[0]), getter, setter)
            )

    return properties

