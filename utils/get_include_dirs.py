
def get_include_dirs() -> Sequence[str]:
    """Gets the include directory for compiling against exported C libraries.

    Depending on how the package was build, development C libraries may or may
    not be present.
    """
    return [os.path.join(_this_dir, "include")]

