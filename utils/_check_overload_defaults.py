
def _check_overload_defaults(impl_defaults, overload_defaults, loc):
    for name, overload_value in overload_defaults.items():
        if name not in impl_defaults or impl_defaults[name] != overload_value:
            raise torch.jit.frontend.FrontendError(
                loc,
                "Default parameters on overloads do not affect the runtime so they "
                "must equal to the default parameter on the implementation function. Found on "
                f"parameter {name}",
            )

