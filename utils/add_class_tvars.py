
def add_class_tvars(
    t: ProperType,
    isuper: Instance | None,
    is_classmethod: bool,
    mx: MemberContext,
    original_vars: Sequence[TypeVarLikeType] | None = None,
    is_trivial_self: bool = False,
) -> Type:
    """Instantiate type variables during analyze_class_attribute_access,
    e.g T and Q in the following:

    class A(Generic[T]):
        @classmethod
        def foo(cls: Type[Q]) -> Tuple[T, Q]: ...

    class B(A[str]): pass
    B.foo()

    Args:
        t: Declared type of the method (or property)
        isuper: Current instance mapped to the superclass where method was defined, this
            is usually done by map_instance_to_supertype()
        is_classmethod: True if this method is decorated with @classmethod
        original_vars: Type variables of the class callable on which the method was accessed
        is_trivial_self: if True, we can use fast path for bind_self().
    Returns:
        Expanded method type with added type variables (when needed).
    """
    # TODO: verify consistency between Q and T

    # We add class type variables if the class method is accessed on class object
    # without applied type arguments, this matches the behavior of __init__().
    # For example (continuing the example in docstring):
    #     A       # The type of callable is def [T] () -> A[T], _not_ def () -> A[Any]
    #     A[int]  # The type of callable is def () -> A[int]
    # and
    #     A.foo       # The type is generic def [T] () -> Tuple[T, A[T]]
    #     A[int].foo  # The type is non-generic def () -> Tuple[int, A[int]]
    #
    # This behaviour is useful for defining alternative constructors for generic classes.
    # To achieve such behaviour, we add the class type variables that are still free
    # (i.e. appear in the return type of the class object on which the method was accessed).
    if isinstance(t, CallableType):
        tvars = original_vars if original_vars is not None else []
        if not mx.preserve_type_var_ids:
            t = freshen_all_functions_type_vars(t)
        if is_classmethod and not t.is_bound:
            if is_trivial_self:
                t = bind_self_fast(t, mx.self_type)
            else:
                t = bind_self(t, mx.self_type, is_classmethod=True)
        if isuper is not None:
            t = expand_type_by_instance(t, isuper)
        freeze_all_type_vars(t)
        return t.copy_modified(variables=list(tvars) + list(t.variables))
    elif isinstance(t, Overloaded):
        return Overloaded(
            [
                cast(
                    CallableType,
                    add_class_tvars(item, isuper, is_classmethod, mx, original_vars=original_vars),
                )
                for item in t.items
            ]
        )
    if isuper is not None:
        t = expand_type_by_instance(t, isuper)
    return t

