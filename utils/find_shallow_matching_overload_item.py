
def find_shallow_matching_overload_item(overload: Overloaded, call: CallExpr) -> CallableType:
    """Perform limited lookup of a matching overload item.

    Full overload resolution is only supported during type checking, but plugins
    sometimes need to resolve overloads. This can be used in some such use cases.

    Resolve overloads based on these things only:

    * Match using argument kinds and names
    * If formal argument has type None, only accept the "None" expression in the callee
    * If formal argument has type Literal[True] or Literal[False], only accept the
      relevant bool literal

    Return the first matching overload item, or the last one if nothing matches.
    """
    for item in overload.items[:-1]:
        ok = True
        mapped = map_actuals_to_formals(
            call.arg_kinds,
            call.arg_names,
            item.arg_kinds,
            item.arg_names,
            lambda i: AnyType(TypeOfAny.special_form),
        )

        # Look for extra actuals
        matched_actuals = set()
        for actuals in mapped:
            matched_actuals.update(actuals)
        if any(i not in matched_actuals for i in range(len(call.args))):
            ok = False

        for arg_type, kind, actuals in zip(item.arg_types, item.arg_kinds, mapped):
            if kind.is_required() and not actuals:
                # Missing required argument
                ok = False
                break
            elif actuals:
                args = [call.args[i] for i in actuals]
                arg_type = get_proper_type(arg_type)
                arg_none = any(isinstance(arg, NameExpr) and arg.name == "None" for arg in args)
                if isinstance(arg_type, NoneType):
                    if not arg_none:
                        ok = False
                        break
                elif (
                    arg_none
                    and not is_overlapping_none(arg_type)
                    and not (
                        isinstance(arg_type, Instance)
                        and arg_type.type.fullname == "builtins.object"
                    )
                    and not isinstance(arg_type, AnyType)
                ):
                    ok = False
                    break
                elif isinstance(arg_type, LiteralType) and isinstance(arg_type.value, bool):
                    if not any(parse_bool(arg) == arg_type.value for arg in args):
                        ok = False
                        break
        if ok:
            return item
    return overload.items[-1]

