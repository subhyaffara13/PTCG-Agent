
def validate_instance(t: Instance, fail: MsgCallback, indexed: bool) -> bool:
    """Check if this is a well-formed instance with respect to argument count/positions."""
    # TODO: combine logic with instantiate_type_alias().
    if any(unknown_unpack(a) for a in t.args):
        # This type is not ready to be validated, because of unknown total count.
        # TODO: is it OK to fill with TypeOfAny.from_error instead of special form?
        return False
    empty_tuple_index = indexed and not t.args
    if t.type.has_type_var_tuple_type:
        min_tv_count = sum(
            not tv.has_default() and not isinstance(tv, TypeVarTupleType)
            for tv in t.type.defn.type_vars
        )
        correct = len(t.args) >= min_tv_count
        if any(
            isinstance(a, UnpackType) and isinstance(get_proper_type(a.type), Instance)
            for a in t.args
        ):
            correct = True
        if not t.args:
            if not (empty_tuple_index and len(t.type.type_vars) == 1):
                # The Any arguments should be set by the caller.
                if empty_tuple_index and min_tv_count:
                    fail(
                        f"At least {min_tv_count} type argument(s) expected, none given",
                        t,
                        code=codes.TYPE_ARG,
                    )
                return False
        elif not correct:
            fail(
                f"Bad number of arguments, expected: at least {min_tv_count}, given: {len(t.args)}",
                t,
                code=codes.TYPE_ARG,
            )
            return False
        else:
            # We also need to check if we are not performing a type variable tuple split.
            unpack = find_unpack_in_list(t.args)
            if unpack is not None:
                unpack_arg = t.args[unpack]
                assert isinstance(unpack_arg, UnpackType)
                if isinstance(unpack_arg.type, TypeVarTupleType):
                    assert t.type.type_var_tuple_prefix is not None
                    assert t.type.type_var_tuple_suffix is not None
                    exp_prefix = t.type.type_var_tuple_prefix
                    act_prefix = unpack
                    exp_suffix = t.type.type_var_tuple_suffix
                    act_suffix = len(t.args) - unpack - 1
                    if act_prefix < exp_prefix or act_suffix < exp_suffix:
                        fail("TypeVarTuple cannot be split", t, code=codes.TYPE_ARG)
                        return False
    elif any(isinstance(a, UnpackType) for a in t.args):
        # A variadic unpack in fixed size instance (fixed unpacks must be flattened by the caller)
        fail(message_registry.INVALID_UNPACK_POSITION, t, code=codes.VALID_TYPE)
        t.args = ()
        return False
    elif len(t.args) != len(t.type.type_vars):
        # Invalid number of type parameters.
        arg_count = len(t.args)
        min_tv_count = sum(not tv.has_default() for tv in t.type.defn.type_vars)
        max_tv_count = len(t.type.type_vars)
        if (arg_count or empty_tuple_index) and (
            arg_count < min_tv_count or arg_count > max_tv_count
        ):
            fail(
                wrong_type_arg_count(min_tv_count, max_tv_count, str(arg_count), t.type.name),
                t,
                code=codes.TYPE_ARG,
            )
        return False
    return True

