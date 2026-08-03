import sys

def setup_mypycify_vars() -> None:
    """Rewrite a bunch of config vars in pretty dubious ways."""
    # There has to be a better approach to this.

    # The vars can contain ints but we only work with str ones
    vars = cast(dict[str, str], sysconfig.get_config_vars())
    if sys.platform == "darwin":
        # Disable building 32-bit binaries, since we generate too much code
        # for a 32-bit Mach-O object. There has to be a better way to do this.
        vars["LDSHARED"] = vars["LDSHARED"].replace("-arch i386", "")
        vars["LDFLAGS"] = vars["LDFLAGS"].replace("-arch i386", "")
        vars["CFLAGS"] = vars["CFLAGS"].replace("-arch i386", "")

