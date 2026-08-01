
def _make_attr_tuple_class(cls_name: str, attr_names: list[str]) -> type:
    """
    Create a tuple subclass to hold `Attribute`s for an `attrs` class.

    The subclass is a bare tuple with properties for names.

    class MyClassAttributes(tuple):
        __slots__ = ()
        x = property(itemgetter(0))
    """
    attr_class_name = f"{cls_name}Attributes"
    body = {}
    for i, attr_name in enumerate(attr_names):

        def getter(self, i=i):
            return self[i]

        body[attr_name] = property(getter)
    return type(attr_class_name, (tuple,), body)

