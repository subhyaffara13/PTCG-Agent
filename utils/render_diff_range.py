
def render_diff_range(
    ranges: list[tuple[int, int]],
    content: list[str],
    *,
    colour: str | None = None,
    output: IO[str] = sys.stderr,
    indent: int = 2,
) -> None:
    for i, line_range in enumerate(ranges):
        is_matching = i % 2 == 1
        lines = content[line_range[0] : line_range[1]]
        for j, line in enumerate(lines):
            if (
                is_matching
                # elide the middle of matching blocks
                and j >= 3
                and j < len(lines) - 3
            ):
                if j == 3:
                    output.write(" " * indent + "...\n")
                continue

            if not is_matching and colour:
                output.write(colour)

            output.write(" " * indent + line)

            if not is_matching:
                if colour:
                    output.write("\033[0m")
                output.write(" (diff)")

            output.write("\n")

