import subprocess
import sys

def initsysfonts_unix(path="fc-list"):
    """use the fc-list from fontconfig to get a list of fonts"""
    fonts = {}

    if sys.platform == "emscripten":
        return fonts

    try:
        proc = subprocess.run(
            [path, ":", "file", "family", "style"],
            stdout=subprocess.PIPE,  # capture stdout
            stderr=subprocess.PIPE,  # capture stderr
            check=True,  # so that errors raise python exception which is handled below
            timeout=1,  # so that we don't hang the program waiting
        )

    except FileNotFoundError:
        warnings.warn(
            f"'{path}' is missing, system fonts cannot be loaded on your platform"
        )

    except subprocess.TimeoutExpired:
        warnings.warn(
            f"Process running '{path}' timed-out! System fonts cannot be loaded on "
            "your platform"
        )

    except subprocess.CalledProcessError as e:
        warnings.warn(
            f"'{path}' failed with error code {e.returncode}! System fonts cannot be "
            f"loaded on your platform. Error log is:\n{e.stderr}"
        )

    else:
        for entry in proc.stdout.decode("ascii", "ignore").splitlines():
            try:
                _parse_font_entry_unix(entry, fonts)
            except ValueError:  # noqa: PERF203
                # try the next one.
                pass

    return fonts

