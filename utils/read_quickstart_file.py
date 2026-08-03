from typing import Any

def read_quickstart_file(
    options: Options, stdout: TextIO
) -> dict[str, tuple[float, int, str]] | None:
    quickstart: dict[str, tuple[float, int, str]] | None = None
    if options.quickstart_file:
        # This is very "best effort". If the file is missing or malformed,
        # just ignore it.
        raw_quickstart: dict[str, Any] = {}
        try:
            with open(options.quickstart_file, "rb") as f:
                raw_quickstart = json_loads(f.read())

            quickstart = {}
            for file, (x, y, z) in raw_quickstart.items():
                quickstart[file] = (x, y, z)
        except Exception as e:
            print(f"Warning: Failed to load quickstart file: {str(e)}\n", file=stdout)
    return quickstart

