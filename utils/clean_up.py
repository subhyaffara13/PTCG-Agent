import os
import re

def clean_up(app, exception):  # noqa: ARG001
    (DIR / "readme.rst").unlink()


def clean_up(a: list[str]) -> list[str]:
    """Remove common directory prefix from all strings in a.

    This uses a naive string replace; it seems to work well enough. Also
    remove trailing carriage returns.
    """
    res = []
    pwd = os.getcwd()
    driver = pwd + "/driver.py"
    for s in a:
        prefix = os.sep
        ss = s
        for p in prefix, prefix.replace(os.sep, "/"):
            if p != "/" and p != "//" and p != "\\" and p != "\\\\":
                ss = ss.replace(p, "")
        # Replace memory address with zeros
        if "at 0x" in ss:
            ss = re.sub(r"(at 0x)\w+>", r"\g<1>000000000000>", ss)
        # Ignore spaces at end of line.
        ss = re.sub(" +$", "", ss)
        # Remove pwd from driver.py's path
        ss = ss.replace(driver, "driver.py")
        res.append(re.sub("\\r$", "", ss))
    return res


def clean_up():
  if xb._default_backend is not None:
    clear_backends(_crash=True)
  clear_caches()

  # Shut down distributed system if it exists. Otherwise, this is a no-op.
  distributed.shutdown()

