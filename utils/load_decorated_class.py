
def load_decorated_class(builder: IRBuilder, cdef: ClassDef, type_obj: Value) -> Value:
    """Apply class decorators to create a decorated (non-extension) class object.

    Given a decorated ClassDef and a register containing a
    non-extension representation of the ClassDef created via the type
    constructor, applies the corresponding decorator functions on that
    decorated ClassDef and returns a register containing the decorated
    ClassDef.
    """
    decorators = cdef.decorators
    dec_class = type_obj
    for d in reversed(decorators):
        decorator = d.accept(builder.visitor)
        assert isinstance(decorator, Value), decorator
        dec_class = builder.py_call(decorator, [dec_class], dec_class.line)
    return dec_class

