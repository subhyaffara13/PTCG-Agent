
def check_specifier(dist, attr, value):
    """Verify that value is a valid version specifier"""
    try:
        SpecifierSet(value)
    except (InvalidSpecifier, AttributeError) as error:
        msg = f"{attr!r} must be a string containing valid version specifiers; {error}"
        raise DistutilsSetupError(msg) from error

