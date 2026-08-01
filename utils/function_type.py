
def function_type(func: FuncBase, fallback: Instance) -> FunctionLike:
    if func.type:
        assert isinstance(func.type, FunctionLike)
        return func.type
    else:
        # Implicit type signature with dynamic types.
        if isinstance(func, FuncItem):
            return callable_type(func, fallback)
        else:
            # Either a broken overload, or decorated overload type is not ready.
            # TODO: make sure the caller defers if possible.
            assert isinstance(func, OverloadedFuncDef)
            any_type = AnyType(TypeOfAny.from_error)
            dummy = CallableType(
                [any_type, any_type],
                [ARG_STAR, ARG_STAR2],
                [None, None],
                any_type,
                fallback,
                line=func.line,
                is_ellipsis_args=True,
            )
            # Return an Overloaded, because some callers may expect that
            # an OverloadedFuncDef has an Overloaded type.
            return Overloaded([dummy])

