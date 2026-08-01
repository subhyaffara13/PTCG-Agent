
def bind_self(
    method: F,
    original_type: Type | None = None,
    is_classmethod: bool = False,
    ignore_instances: bool = False,
) -> F:
    """Return a copy of `method`, with the type of its first parameter (usually
    self or cls) bound to original_type.

    If the type of `self` is a generic type (T, or Type[T] for classmethods),
    instantiate every occurrence of type with original_type in the rest of the
    signature and in the return type.

    original_type is the type of E in the expression E.copy(). It is None in
    compatibility checks. In this case we treat it as the erasure of the
    declared type of self.

    This way we can express "the type of self". For example:

    T = TypeVar('T', bound='A')
    class A:
        def copy(self: T) -> T: ...

    class B(A): pass

    b = B().copy()  # type: B

    """
    if isinstance(method, Overloaded):
        items = [
            bind_self(c, original_type, is_classmethod, ignore_instances) for c in method.items
        ]
        return cast(F, Overloaded(items))
    assert isinstance(method, CallableType)
    func: CallableType = method
    if not func.arg_types:
        # Invalid method, return something.
        return method
    if func.arg_kinds[0] in (ARG_STAR, ARG_STAR2):
        # The signature is of the form 'def foo(*args, ...)'.
        # In this case we shouldn't drop the first arg,
        # since func will be absorbed by the *args.
        # TODO: infer bounds on the type of *args?

        # In the case of **kwargs we should probably emit an error, but
        # for now we simply skip it, to avoid crashes down the line.
        return method
    self_param_type = get_proper_type(func.arg_types[0])

    variables: Sequence[TypeVarLikeType]
    # Having a def __call__(self: Callable[...], ...) can cause infinite recursion. Although
    # this special-casing looks not very principled, there is nothing meaningful we can infer
    # from such definition, since it is inherently indefinitely recursive.
    allow_callable = func.name is None or not func.name.startswith("__call__ of")
    if func.variables and supported_self_type(
        self_param_type, allow_callable=allow_callable, allow_instances=not ignore_instances
    ):
        from mypy.infer import infer_type_arguments

        if original_type is None:
            # TODO: type check method override (see #7861).
            original_type = erase_to_bound(self_param_type)
        original_type = get_proper_type(original_type)

        # Find which of method type variables appear in the type of "self".
        self_ids = {tv.id for tv in get_all_type_vars(self_param_type)}
        self_vars = [tv for tv in func.variables if tv.id in self_ids]

        # Solve for these type arguments using the actual class or instance type.
        typeargs = infer_type_arguments(
            self_vars, self_param_type, original_type, is_supertype=True, erase_types=False
        )
        if (
            is_classmethod
            and any(isinstance(get_proper_type(t), UninhabitedType) for t in typeargs)
            and isinstance(original_type, (Instance, TypeVarType, TupleType))
        ):
            # In case we call a classmethod through an instance x, fallback to type(x).
            typeargs = infer_type_arguments(
                self_vars,
                self_param_type,
                TypeType(original_type),
                is_supertype=True,
                erase_types=False,
            )

        # Update the method signature with the solutions found.
        # Technically, some constraints might be unsolvable, make them Never.
        to_apply = [t if t is not None else UninhabitedType() for t in typeargs]
        func = expand_type(func, {tv.id: arg for tv, arg in zip(self_vars, to_apply)})
        variables = [v for v in func.variables if v not in self_vars]
    else:
        variables = func.variables

    res = func.copy_modified(
        arg_types=func.arg_types[1:],
        arg_kinds=func.arg_kinds[1:],
        arg_names=func.arg_names[1:],
        variables=variables,
        is_bound=True,
    )
    return cast(F, res)

