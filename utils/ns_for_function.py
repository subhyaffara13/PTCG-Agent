from typing import Any, Callable

def ns_for_function(obj: Callable[..., Any], parent_namespace: MappingNamespace | None = None) -> NamespacesTuple:
    """Return the global and local namespaces to be used when evaluating annotations for the provided function.

    The global namespace will be the `__dict__` attribute of the module the function was defined in.
    The local namespace will contain the `__type_params__` introduced by PEP 695.

    Args:
        obj: The object to use when building namespaces.
        parent_namespace: Optional namespace to be added with the lowest priority in the local namespace.
            If the passed function is a method, the `parent_namespace` will be the namespace of the class
            the method is defined in. Thus, we also fetch type `__type_params__` from there (i.e. the
            class-scoped type variables).
    """
    locals_list: list[MappingNamespace] = []
    if parent_namespace is not None:
        locals_list.append(parent_namespace)

    # Get the `__type_params__` attribute introduced by PEP 695.
    # Note that the `typing._eval_type` function expects type params to be
    # passed as a separate argument. However, internally, `_eval_type` calls
    # `ForwardRef._evaluate` which will merge type params with the localns,
    # essentially mimicking what we do here.
    type_params: tuple[_TypeVarLike, ...] = getattr(obj, '__type_params__', ())
    if parent_namespace is not None:
        # We also fetch type params from the parent namespace. If present, it probably
        # means the function was defined in a class. This is to support the following:
        # https://github.com/python/cpython/issues/124089.
        type_params += parent_namespace.get('__type_params__', ())

    locals_list.append({t.__name__: t for t in type_params})

    # What about short-circuiting to `obj.__globals__`?
    globalns = get_module_ns_of(obj)

    return NamespacesTuple(globalns, LazyLocalNamespace(*locals_list))

