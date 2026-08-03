import json
import os
import sys
from typing import Any

def check_output(
    response: dict[str, Any], verbose: bool, junit_xml: str | None, perf_stats_file: str | None
) -> None:
    """Print the output from a check or recheck command.

    Call sys.exit() unless the status code is zero.
    """
    if os.name == "nt":
        # Enable ANSI color codes for Windows cmd using this strange workaround
        # ( see https://github.com/python/cpython/issues/74261 )
        os.system("")
    if "error" in response:
        fail(response["error"])
    try:
        out, err, status_code = response["out"], response["err"], response["status"]
    except KeyError:
        fail(f"Response: {str(response)}")
    sys.stdout.write(out)
    sys.stdout.flush()
    sys.stderr.write(err)
    sys.stderr.flush()
    if verbose:
        show_stats(response)
    if junit_xml:
        # Lazy import so this import doesn't slow things down when not writing junit
        from mypy.util import write_junit_xml

        messages = (out + err).splitlines()
        write_junit_xml(
            response["roundtrip_time"],
            bool(err),
            {None: messages} if messages else {},
            junit_xml,
            response["python_version"],
            response["platform"],
        )
    if perf_stats_file:
        telemetry = response.get("stats", {})
        with open(perf_stats_file, "w") as f:
            json.dump(telemetry, f)

    if status_code:
        sys.exit(status_code)

