import re
from typing import Union

def parse_version(v: str | float) -> tuple[int, int]:
    m = re.match(r"\A(\d)\.(\d+)\Z", str(v))
    if not m:
        raise argparse.ArgumentTypeError(f"Invalid python version '{v}' (expected format: 'x.y')")
    major, minor = int(m.group(1)), int(m.group(2))
    if major == 2 and minor == 7:
        pass  # Error raised elsewhere
    elif major == 3:
        if minor < defaults.PYTHON3_VERSION_MIN[1]:
            msg = "Python 3.{} is not supported (must be {}.{} or higher)".format(
                minor, *defaults.PYTHON3_VERSION_MIN
            )

            if isinstance(v, float):
                msg += ". You may need to put quotes around your Python version"

            raise VersionTypeError(msg, fallback=defaults.PYTHON3_VERSION_MIN)
    else:
        raise argparse.ArgumentTypeError(
            f"Python major version '{major}' out of range (must be 3)"
        )
    return major, minor


def parse_version(version: str) -> tuple[int, int]:
    major, minor = version.strip().split(".")
    return int(major), int(minor)


def parse_version(version_str: str) -> tuple[Union[int, str], ...]:
    version: list[Union[int, str]] = []
    for part in version_str.split('.'):
        try:
            version.append(int(part))
        except ValueError:
            version.append(part)

    return tuple(version)


def parse_version(version: int) -> tuple[int, int, int]:
    x = (version & 0xFFFF0000) >> 16
    y = (version & 0x0000FF00) >> 8
    z = version & 0x000000FF
    return x, y, z


def parse_version(v: str) -> tuple[int, ...]:
  m = _version_regex.match(v)
  if m is None:
    raise ValueError(f"Unable to parse version '{v}'")
  return tuple(int(x) for x in m.group(1).split('.'))

