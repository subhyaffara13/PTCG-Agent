
def type_object_type_from_function(
    signature: FunctionLike, info: TypeInfo, def_info: TypeInfo, fallback: Instance, is_new: bool
) -> FunctionLike:
    # We first need to record all non-trivial (explicit) self types in __init__,
    # since they will not be available after we bind them. Note, we use explicit
    # self-types only in the defining class, similar to __new__ (but not exactly the same,
    # see comment in class_callable below). This is mostly useful for annotating library
    # classes such as subprocess.Popen.
    if not is_new and not info.is_newtype:
        orig_self_types = [get_self_type(it, def_info) for it in signature.items]
    else:
        orig_self_types = [None] * len(signature.items)

    # The __init__ method might come from a generic superclass 'def_info'
    # with type variables that do not map identically to the type variables of
    # the class 'info' being constructed. For example:
    #
    #   class A(Generic[T]):
    #       def __init__(self, x: T) -> None: ...
    #   class B(A[List[T]]):
    #      ...
    #
    # We need to map B's __init__ to the type (List[T]) -> None.
    signature = bind_self(
        signature,
        original_type=fill_typevars(info),
        is_classmethod=is_new,
        # Explicit instance self annotations have special handling in class_callable(),
        # we don't need to bind any type variables in them if they are generic.
        ignore_instances=True,
    )
    signature = cast(FunctionLike, map_type_from_supertype(signature, info, def_info))

    special_sig: str | None = None
    if def_info.fullname == "builtins.dict":
        # Special signature!
        special_sig = "dict"

    if isinstance(signature, CallableType):
        return class_callable(
            signature, info, def_info, fallback, special_sig, is_new, orig_self_types[0]
        )
    else:
        # Overloaded __init__/__new__.
        assert isinstance(signature, Overloaded)
        items: list[CallableType] = []
        for item, orig_self in zip(signature.items, orig_self_types):
            items.append(
                class_callable(item, info, def_info, fallback, special_sig, is_new, orig_self)
            )
        return Overloaded(items)

