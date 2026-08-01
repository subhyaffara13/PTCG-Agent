
def can_subclass_builtin(builtin_base: str) -> bool:
    # BaseException and dict are special cased.
    return builtin_base in (
        (
            "builtins.Exception",
            "builtins.LookupError",
            "builtins.IndexError",
            "builtins.Warning",
            "builtins.UserWarning",
            "builtins.ValueError",
            "builtins.object",
        )
    )

