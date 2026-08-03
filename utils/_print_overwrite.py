import sys

def _print_overwrite(report: str) -> None:
    """Print a report, overwriting the previous lines.

    Since tqdm in using `sys.stderr` to (re-)write progress bars, we need to use `sys.stdout`
    to print the report.

    Note: works well only if no other process is writing to `sys.stdout`!
    """
    report += "\n"
    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns

    # Count number of lines that should be cleared
    nb_lines = sum(len(line) // terminal_width + 1 for line in report.splitlines())

    # Clear previous lines based on the number of lines in the report
    for _ in range(nb_lines):
        sys.stdout.write("\r\033[K")  # Clear line
        sys.stdout.write("\033[F")  # Move cursor up one line

    # Print the new report, filling remaining space with whitespace
    sys.stdout.write(report)
    sys.stdout.write(" " * (terminal_width - len(report.splitlines()[-1])))
    sys.stdout.flush()

