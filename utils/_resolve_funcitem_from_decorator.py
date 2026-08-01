
def _resolve_funcitem_from_decorator(dec: nodes.OverloadPart) -> nodes.FuncItem | None:
    """Returns a FuncItem that corresponds to the output of the decorator.

    Returns None if we can't figure out what that would be. For convenience, this function also
    accepts FuncItems.
    """
    if isinstance(dec, nodes.FuncItem):
        return dec
    if dec.func.is_property:
        return None

    def apply_decorator_to_funcitem(
        decorator: nodes.Expression, func: nodes.FuncItem
    ) -> nodes.FuncItem | None:
        if (
            isinstance(decorator, nodes.CallExpr)
            and isinstance(decorator.callee, nodes.RefExpr)
            and decorator.callee.fullname in mypy.types.DEPRECATED_TYPE_NAMES
        ):
            return func
        if not isinstance(decorator, nodes.RefExpr):
            return None
        if not decorator.fullname:
            # Happens with namedtuple
            return None
        if (
            decorator.fullname in ("builtins.staticmethod", "abc.abstractmethod")
            or decorator.fullname in mypy.types.OVERLOAD_NAMES
            or decorator.fullname in mypy.types.OVERRIDE_DECORATOR_NAMES
            or decorator.fullname in mypy.types.FINAL_DECORATOR_NAMES
        ):
            return func
        if decorator.fullname == "builtins.classmethod":
            if func.arguments[0].variable.name not in ("_cls", "cls", "mcs", "metacls"):
                raise StubtestFailure(
                    f"unexpected class parameter name {func.arguments[0].variable.name!r} "
                    f"in {dec.fullname}"
                )
            # FuncItem is written so that copy.copy() actually works, even when compiled
            ret = copy.copy(func)
            # Remove the cls argument, since it's not present in inspect.signature of classmethods
            ret.arguments = ret.arguments[1:]
            return ret
        # Just give up on any other decorators. After excluding properties, we don't run into
        # anything else when running on typeshed's stdlib.
        return None

    func: nodes.FuncItem = dec.func
    for decorator in dec.original_decorators:
        resulting_func = apply_decorator_to_funcitem(decorator, func)
        if resulting_func is None:
            # We couldn't figure out how to apply the decorator by transforming nodes, so try to
            # reconstitute a FuncDef from the resulting type of the decorator
            # This is worse because e.g. we lose the values of defaults
            dec_type = mypy.types.get_proper_type(dec.type)
            callable_type = None
            if isinstance(dec_type, mypy.types.Instance):
                callable_type = mypy.subtypes.find_member(
                    "__call__", dec_type, dec_type, is_operator=True
                )
            elif isinstance(dec_type, mypy.types.CallableType):
                callable_type = dec_type

            callable_type = mypy.types.get_proper_type(callable_type)
            if isinstance(callable_type, mypy.types.CallableType):
                return _resolve_funcitem_from_callable_type(dec, callable_type)
            return None

        func = resulting_func
    return func

