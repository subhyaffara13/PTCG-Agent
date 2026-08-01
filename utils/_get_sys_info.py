
def _get_sys_info():
    """
    Get useful system information.

    Returns
    -------
    dict
        Useful system information.
    """
    return {
        "python": sys.version.replace(os.linesep, " "),
        "executable": sys.executable,
        "machine": platform.platform(),
    }


def _get_sys_info() -> dict[str, JSONSerializable]:
    """
    Returns system information as a JSON serializable dictionary.
    """
    uname_result = platform.uname()
    language_code, encoding = locale.getlocale()
    return {
        "commit": _get_commit_hash(),
        "python": platform.python_version(),
        "python-bits": struct.calcsize("P") * 8,
        "OS": uname_result.system,
        "OS-release": uname_result.release,
        "Version": uname_result.version,
        "machine": uname_result.machine,
        "processor": uname_result.processor,
        "byteorder": sys.byteorder,
        "LC_ALL": os.environ.get("LC_ALL"),
        "LANG": os.environ.get("LANG"),
        "LOCALE": {"language-code": language_code, "encoding": encoding},
    }

