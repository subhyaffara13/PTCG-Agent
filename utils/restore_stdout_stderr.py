import sys

def restore_stdout_stderr() -> Iterator[None]:
    initial_stdout, initial_stderr = sys.stdout, sys.stderr
    try:
        yield
    finally:
        sys.stdout, sys.stderr = initial_stdout, initial_stderr

