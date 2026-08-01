
def _install_setup_requires(attrs):
    # Note: do not use `setuptools.Distribution` directly, as
    # our PEP 517 backend patch `distutils.core.Distribution`.
    class MinimalDistribution(distutils.core.Distribution):
        """
        A minimal version of a distribution for supporting the
        fetch_build_eggs interface.
        """

        def __init__(self, attrs: Mapping[str, object]) -> None:
            _incl = 'dependency_links', 'setup_requires'
            filtered = {k: attrs[k] for k in set(_incl) & set(attrs)}
            super().__init__(filtered)
            # Prevent accidentally triggering discovery with incomplete set of attrs
            self.set_defaults._disable()

        def _get_project_config_files(self, filenames=None):
            """Ignore ``pyproject.toml``, they are not related to setup_requires"""
            try:
                cfg, _toml = super()._split_standard_project_metadata(filenames)
            except Exception:
                return filenames, ()
            return cfg, ()

        def finalize_options(self):
            """
            Disable finalize_options to avoid building the working set.
            Ref #2158.
            """

    dist = MinimalDistribution(attrs)

    # Honor setup.cfg's options.
    dist.parse_config_files(ignore_option_errors=True)
    if dist.setup_requires:
        _fetch_build_eggs(dist)

