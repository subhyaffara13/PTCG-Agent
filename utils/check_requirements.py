
def check_requirements(dist, attr: str, value: _OrderedStrSequence) -> None:
    """Verify that install_requires is a valid requirements list"""
    try:
        list(_reqs.parse(value))
        if isinstance(value, set):
            raise TypeError("Unordered types are not allowed")
    except (TypeError, ValueError) as error:
        msg = (
            f"{attr!r} must be a string or iterable of strings "
            f"containing valid project/version requirement specifiers; {error}"
        )
        raise DistutilsSetupError(msg) from error

