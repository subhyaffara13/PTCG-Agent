import sys

def dump_original_errors(errors: list[str]) -> None:
    sys.stderr.write("Original errors:\n")
    for err in errors:
        sys.stderr.write(err + "\n")

