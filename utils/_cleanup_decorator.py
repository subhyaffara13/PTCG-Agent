
def _cleanup_decorator(stmt: Decorator, attr_map: dict[str, Attribute]) -> None:
    """Handle decorators in class bodies.

    `x.default` will set a default value on x
    `x.validator` and `x.default` will get removed to avoid throwing a type error.
    """
    remove_me = []
    for func_decorator in stmt.decorators:
        if (
            isinstance(func_decorator, MemberExpr)
            and isinstance(func_decorator.expr, NameExpr)
            and func_decorator.expr.name in attr_map
        ):
            if func_decorator.name == "default":
                attr_map[func_decorator.expr.name].has_default = True

            if func_decorator.name in ("default", "validator"):
                # These are decorators on the attrib object that only exist during
                # class creation time.  In order to not trigger a type error later we
                # just remove them.  This might leave us with a Decorator with no
                # decorators (Emperor's new clothes?)
                # TODO: It would be nice to type-check these rather than remove them.
                #       default should be Callable[[], T]
                #       validator should be Callable[[Any, 'Attribute', T], Any]
                #       where T is the type of the attribute.
                remove_me.append(func_decorator)
    for dec in remove_me:
        stmt.decorators.remove(dec)

