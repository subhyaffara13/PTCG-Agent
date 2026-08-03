from typing import Callable

def type_object_type(
    info: TypeInfo, named_type: Callable[[str], Instance] | None = None
) -> ProperType:
    """Return the type of a type object.

    For a generic type G with type variables T and S the type is generally of form

      Callable[..., G[T, S]]

    where ... are argument types for the __init__/__new__ method (without the self
    argument). Also, the fallback type will be 'type' instead of 'function'.
    Note: we keep the unused `named_type` argument to avoid breaking plugins.
    """
    allow_cache = (
        checker_state.type_checker is not None
        and checker_state.type_checker.allow_constructor_cache
    )

    if info.type_object_type is not None:
        if allow_cache:
            return info.type_object_type
        info.type_object_type = None

    # We take the type from whichever of __init__ and __new__ is first
    # in the MRO, preferring __init__ if there is a tie.
    init_method = info.get("__init__")
    new_method = info.get("__new__")
    if not init_method or not is_valid_constructor(init_method.node):
        # Must be an invalid class definition.
        return AnyType(TypeOfAny.from_error)
    # There *should* always be a __new__ method except the test stubs
    # lack it, so just copy init_method in that situation
    new_method = new_method or init_method
    if not is_valid_constructor(new_method.node):
        # Must be an invalid class definition.
        return AnyType(TypeOfAny.from_error)

    # The two is_valid_constructor() checks ensure this.
    assert isinstance(new_method.node, (SYMBOL_FUNCBASE_TYPES, Decorator))
    assert isinstance(init_method.node, (SYMBOL_FUNCBASE_TYPES, Decorator))

    init_index = info.mro.index(init_method.node.info)
    new_index = info.mro.index(new_method.node.info)

    if info.metaclass_type is not None:
        fallback = info.metaclass_type
    else:
        type_type = lookup_stdlib_typeinfo("builtins.type", modules_state.modules)
        fallback = Instance(type_type, [])

    if init_index < new_index:
        method: FuncBase | Decorator = init_method.node
        is_new = False
    elif init_index > new_index:
        method = new_method.node
        is_new = True
    else:
        if init_method.node.info.fullname == "builtins.object":
            # Both are defined by object.  But if we've got a bogus
            # base class, we can't know for sure, so check for that.
            if info.fallback_to_any:
                # Construct a universal callable as the prototype.
                any_type = AnyType(TypeOfAny.special_form)
                if instance_cache.function_type is None:
                    function_typeinfo = lookup_stdlib_typeinfo(
                        "builtins.function", modules_state.modules
                    )
                    instance_cache.function_type = Instance(function_typeinfo, [])
                sig = CallableType(
                    arg_types=[any_type, any_type],
                    arg_kinds=[ARG_STAR, ARG_STAR2],
                    arg_names=["_args", "_kwds"],
                    ret_type=any_type,
                    is_bound=True,
                    fallback=instance_cache.function_type,
                )
                result: FunctionLike = class_callable(
                    sig, info, None, fallback, None, is_new=False
                )
                if allow_cache and state.strict_optional:
                    info.type_object_type = result
                return result

        # Otherwise prefer __init__ in a tie. It isn't clear that this
        # is the right thing, but __new__ caused problems with
        # typeshed (#5647).
        method = init_method.node
        is_new = False
    # Construct callable type based on signature of __init__. Adjust
    # return type and insert type arguments.
    if isinstance(method, FuncBase):
        if isinstance(method, OverloadedFuncDef) and not method.type:
            # Do not cache if the type is not ready. Same logic for decorators is
            # achieved in early return above because is_valid_constructor() is False.
            allow_cache = False
        t = function_type(method, fallback)
    else:
        assert isinstance(method.type, ProperType)
        assert isinstance(method.type, FunctionLike)  # is_valid_constructor() ensures this
        t = method.type
    result = type_object_type_from_function(t, info, method.info, fallback, is_new)
    # Tuple constructor in typeshed is imprecise (and precise one is impossible to express),
    # so we special-case constructors for tuple types. Note we skip the tuple class itself
    # as a micro-optimization, since it is unlikely one would write tuple((1, 2)).
    if method.info.fullname == "builtins.tuple" and info.fullname != "builtins.tuple":
        assert isinstance(result, CallableType)
        result = result.copy_modified(special_sig="tuple")
    # Only write cached result is strict_optional=True, otherwise we may get
    # inconsistent behaviour because of union simplification.
    if allow_cache and state.strict_optional:
        info.type_object_type = result
    return result

