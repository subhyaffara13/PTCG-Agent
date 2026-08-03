import subprocess

def get_gcc_major_version():
    """
    Return GCC major version as int, or None if GCC is not available.
    """
    try:
        out = subprocess.check_output(
            ["gcc", "-dumpfullversion", "-dumpversion"],
            stderr=subprocess.STDOUT,
            text=True,
        ).strip()
        return int(out.split(".")[0])
    except Exception:
        return None

