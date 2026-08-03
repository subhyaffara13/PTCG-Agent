from typing import Any

def instantiate_user_defined_class_object(
    cls: type[T], /, *args: Any, **kwargs: Any
) -> T:
    obj = cls.__new__(cls, *args, **kwargs)

    # Only call __init__ if the object's type is a subclass of cls.
    # CPython uses PyType_IsSubtype(Py_TYPE(obj), type) at the C level, which does NOT
    # go through metaclass __instancecheck__. Using isinstance() here would be wrong
    # for classes with custom __instancecheck__ (e.g. torch.ByteStorage).
    # Reference: https://github.com/python/cpython/blob/3.12/Objects/typeobject.c#L1670-L1673
    if issubclass(type(obj), cls):
        obj.__init__(*args, **kwargs)
    return obj

