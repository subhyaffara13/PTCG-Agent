
def get_explicit_package_bases(options: Options) -> list[str] | None:
    """Returns explicit package bases to use if the option is enabled, or None if disabled.

    We currently use MYPYPATH and the current directory as the package bases. In the future,
    when --namespace-packages is the default could also use the values passed with the
    --package-root flag, see #9632.

    Values returned are normalised so we can use simple string comparisons in
    SourceFinder.is_explicit_package_base
    """
    if not options.explicit_package_bases:
        return None
    roots = mypy_path() + options.mypy_path + [os.getcwd()]
    return [normalise_package_base(root) for root in roots]

