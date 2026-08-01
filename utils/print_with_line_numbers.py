
def print_with_line_numbers(s: str) -> None:
    lines = s.splitlines()
    for i, line in enumerate(lines):
        print("%-4d %s" % (i + 1, line))

