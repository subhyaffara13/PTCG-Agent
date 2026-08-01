
def _deprecation_notice(fn: Fn) -> Fn:
    @wraps(fn)
    def _wrapper(*args, **kwargs):
        SetuptoolsDeprecationWarning.emit(
            "Deprecated API usage.",
            f"""
            As setuptools moves its configuration towards `pyproject.toml`,
            `{__name__}.{fn.__name__}` became deprecated.

            For the time being, you can use the `{setupcfg.__name__}` module
            to access a backward compatible API, but this module is provisional
            and might be removed in the future.

            To read project metadata, consider using
            ``build.util.project_wheel_metadata`` (https://pypi.org/project/build/).
            For simple scenarios, you can also try parsing the file directly
            with the help of ``configparser``.
            """,
            # due_date not defined yet, because the community still heavily relies on it
            # Warning introduced in 24 Mar 2022
        )
        return fn(*args, **kwargs)

    return cast(Fn, _wrapper)

