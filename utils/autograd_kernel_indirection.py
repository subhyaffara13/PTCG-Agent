
def autograd_kernel_indirection(custom_op):
    autograd_fallback = autograd_not_implemented(custom_op)

    def inner(*args, **kwargs):
        if custom_op._has_impl("autograd"):
            kernel = custom_op._get_impl("autograd").func
            return kernel(*args, **kwargs)
        # As explained in NOTE ["backward", "save_for_backward", and "autograd"],
        # after the user gives us "backward" and "save_for_backward", we generate
        # the "autograd" impl. If the user only provided one, then we tell
        # the user they've done something wrong.
        if custom_op._has_impl("save_for_backward") or custom_op._has_impl("backward"):
            missing = (
                "save_for_backward" if custom_op._has_impl("backward") else "backward"
            )
            found = "save_for_backward" if missing == "backward" else "backward"
            loc = custom_op._get_impl(found).location
            raise RuntimeError(
                f"We found a '{found}' registration for {custom_op} at "
                f"{loc} but were unable to find a '{missing}' registration. "
                f"To use the CustomOp API to register a backward formula, "
                f"please provide us both a backward function and a "
                f"'save for backward' function via `impl_backward` and "
                f"`impl_save_for_backward` respectively."
            )
        return autograd_fallback(*args, **kwargs)

    return inner

