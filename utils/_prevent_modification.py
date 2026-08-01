
def _prevent_modification(target: type, method: str, copying: str) -> None:
    """
    Because setuptools is very flexible we cannot fully prevent
    plugins and user customizations from modifying static values that were
    parsed from config files.
    But we can attempt to block "in-place" mutations and identify when they
    were done.
    """
    fn = getattr(target, method, None)
    if fn is None:
        return

    @wraps(fn)
    def _replacement(self: Static, *args, **kwargs):
        # TODO: After deprecation period raise NotImplementedError instead of warning
        #       which obviated the existence and checks of the `_mutated_` attribute.
        self._mutated_ = True
        SetuptoolsDeprecationWarning.emit(
            "Direct modification of value will be disallowed",
            f"""
            In an effort to implement PEP 643, direct/in-place changes of static values
            that come from configuration files are deprecated.
            If you need to modify this value, please first create a copy with {copying}
            and make sure conform to all relevant standards when overriding setuptools
            functionality (https://packaging.python.org/en/latest/specifications/).
            """,
            due_date=(2025, 10, 10),  # Initially introduced in 2024-09-06
        )
        return fn(self, *args, **kwargs)

    _replacement.__doc__ = ""  # otherwise doctest may fail.
    setattr(target, method, _replacement)

