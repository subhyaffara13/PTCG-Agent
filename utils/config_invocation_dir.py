
def Config_invocation_dir(self: Config) -> LEGACY_PATH:
    """The directory from which pytest was invoked.

    Prefer to use :attr:`invocation_params.dir <InvocationParams.dir>`,
    which is a :class:`pathlib.Path`.

    :type: LEGACY_PATH
    """
    return legacy_path(str(self.invocation_params.dir))

