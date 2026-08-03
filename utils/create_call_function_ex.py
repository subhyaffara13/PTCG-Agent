import sys

def create_call_function_ex(
    has_kwargs: bool, push_null: bool, ignore_314_kwargs_push: bool = False
) -> list[Instruction]:
    """
    Assumes that in 3.14+, if has_kwargs=False, there is NOT a NULL
    on the TOS for the kwargs. This utility function will add a PUSH_NULL.

    If the caller has already pushed a NULL for the kwargs, then set ignore_314_kwargs_push=True
    so we don't push another NULL for the kwargs.
    """
    if sys.version_info >= (3, 11):
        output = []
        if (
            sys.version_info >= (3, 14)
            and not has_kwargs
            and not ignore_314_kwargs_push
        ):
            output.append(create_instruction("PUSH_NULL"))
            has_kwargs = True
        if push_null:
            output.append(create_instruction("PUSH_NULL"))
            # 3.13 swapped NULL and callable
            # if flags == 1, 2 values popped - otherwise if flags == 0, 1 value
            rots = (
                int(has_kwargs) + 2
                if sys.version_info >= (3, 13)
                else int(has_kwargs) + 3
            )
            output.extend(create_rot_n(rots))
        output.append(create_instruction("CALL_FUNCTION_EX", arg=int(has_kwargs)))
        return output
    return [create_instruction("CALL_FUNCTION_EX", arg=int(has_kwargs))]

