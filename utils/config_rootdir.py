
def Config_rootdir(self: Config) -> LEGACY_PATH:
    """The path to the :ref:`rootdir <rootdir>`.

    Prefer to use :attr:`rootpath`, which is a :class:`pathlib.Path`.

    :type: LEGACY_PATH
    """
    return legacy_path(str(self.rootpath))

