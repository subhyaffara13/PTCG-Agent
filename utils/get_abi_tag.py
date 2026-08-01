
def get_abi_tag() -> str | None:
    """Return the ABI tag based on SOABI (if available) or emulate SOABI (PyPy2)."""
    soabi: str = sysconfig.get_config_var("SOABI")
    impl = tags.interpreter_name()
    if not soabi and impl in ("cp", "pp") and hasattr(sys, "maxunicode"):
        d = ""
        u = ""
        if get_flag("Py_DEBUG", hasattr(sys, "gettotalrefcount"), warn=(impl == "cp")):
            d = "d"

        abi = f"{impl}{tags.interpreter_version()}{d}{u}"
    elif soabi and impl == "cp" and soabi.startswith("cpython"):
        # non-Windows
        abi = "cp" + soabi.split("-")[1]
    elif soabi and impl == "cp" and soabi.startswith("cp"):
        # Windows
        abi = soabi.split("-")[0]
        if hasattr(sys, "gettotalrefcount"):
            # using debug build; append "d" flag
            abi += "d"
    elif soabi and impl == "pp":
        # we want something like pypy36-pp73
        abi = "-".join(soabi.split("-")[:2])
        abi = abi.replace(".", "_").replace("-", "_")
    elif soabi and impl == "graalpy":
        abi = "-".join(soabi.split("-")[:3])
        abi = abi.replace(".", "_").replace("-", "_")
    elif soabi:
        abi = soabi.replace(".", "_").replace("-", "_")
    else:
        abi = None

    return abi


def get_abi_tag() -> str | None:
    """Return the ABI tag based on SOABI (if available) or emulate SOABI (PyPy2)."""
    soabi: str = sysconfig.get_config_var("SOABI")
    impl = tags.interpreter_name()
    if not soabi and impl in ("cp", "pp") and hasattr(sys, "maxunicode"):
        d = ""
        m = ""
        u = ""
        if get_flag("Py_DEBUG", hasattr(sys, "gettotalrefcount"), warn=(impl == "cp")):
            d = "d"

        if get_flag(
            "WITH_PYMALLOC",
            impl == "cp",
            warn=(impl == "cp" and sys.version_info < (3, 8)),
        ) and sys.version_info < (3, 8):
            m = "m"

        abi = f"{impl}{tags.interpreter_version()}{d}{m}{u}"
    elif soabi and impl == "cp" and soabi.startswith("cpython"):
        # non-Windows
        abi = "cp" + soabi.split("-")[1]
    elif soabi and impl == "cp" and soabi.startswith("cp"):
        # Windows
        abi = soabi.split("-")[0]
    elif soabi and impl == "pp":
        # we want something like pypy36-pp73
        abi = "-".join(soabi.split("-")[:2])
        abi = abi.replace(".", "_").replace("-", "_")
    elif soabi and impl == "graalpy":
        abi = "-".join(soabi.split("-")[:3])
        abi = abi.replace(".", "_").replace("-", "_")
    elif soabi:
        abi = soabi.replace(".", "_").replace("-", "_")
    else:
        abi = None

    return abi

