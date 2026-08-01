
def check_nsp(dist, attr, value):
    """Verify that namespace packages are valid"""
    ns_packages = value
    assert_string_list(dist, attr, ns_packages)
    for nsp in ns_packages:
        if not dist.has_contents_for(nsp):
            raise DistutilsSetupError(
                f"Distribution contains no modules or packages for namespace package {nsp!r}"
            )
        parent, _sep, _child = nsp.rpartition('.')
        if parent and parent not in ns_packages:
            distutils.log.warn(
                "WARNING: %r is declared as a package namespace, but %r"
                " is not: please correct this in setup.py",
                nsp,
                parent,
            )
        SetuptoolsDeprecationWarning.emit(
            "The namespace_packages parameter is deprecated.",
            "Please replace its usage with implicit namespaces (PEP 420).",
            see_docs="references/keywords.html#keyword-namespace-packages",
            # TODO: define due_date, it may break old packages that are no longer
            # maintained (e.g. sphinxcontrib extensions) when installed from source.
            # Warning officially introduced in May 2022, however the deprecation
            # was mentioned much earlier in the docs (May 2020, see #2149).
        )

