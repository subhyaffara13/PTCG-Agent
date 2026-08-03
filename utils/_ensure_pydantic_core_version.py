import sys

def _ensure_pydantic_core_version() -> None:  # pragma: no cover
    if not check_pydantic_core_version():
        raise_error = True
        # Do not raise the error if pydantic is installed in editable mode (i.e. in development):
        if sys.version_info >= (3, 13):  # origin property added in 3.13
            from importlib.metadata import distribution

            dist = distribution('pydantic')
            if getattr(getattr(dist.origin, 'dir_info', None), 'editable', False):
                raise_error = False

        if raise_error:
            raise SystemError(
                f'The installed pydantic-core version ({__pydantic_core_version__}) is incompatible '
                f'with the current pydantic version, which requires {_COMPATIBLE_PYDANTIC_CORE_VERSION}. '
                "If you encounter this error, make sure that you haven't upgraded pydantic-core manually."
            )

