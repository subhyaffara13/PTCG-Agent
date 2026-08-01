
def get_lib_location_guesses(
    user: bool = False,
    home: str | None = None,
    root: str | None = None,
    isolated: bool = False,
    prefix: str | None = None,
) -> list[str]:
    scheme = get_scheme(
        "",
        user=user,
        home=home,
        root=root,
        isolated=isolated,
        prefix=prefix,
    )
    return [scheme.purelib, scheme.platlib]

