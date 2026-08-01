
def Config_inifile(self: Config) -> LEGACY_PATH | None:
    """The path to the :ref:`configfile <configfiles>`.

    Prefer to use :attr:`inipath`, which is a :class:`pathlib.Path`.

    :type: Optional[LEGACY_PATH]
    """
    return legacy_path(str(self.inipath)) if self.inipath else None

