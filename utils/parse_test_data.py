
def parse_test_data(raw_data: str, name: str) -> list[TestItem]:
    """Parse a list of lines that represent a sequence of test items."""

    lines = ["", "[case " + name + "]"] + raw_data.split("\n")
    ret: list[TestItem] = []
    data: list[str] = []

    id: str | None = None
    arg: str | None = None

    i = 0
    i0 = 0
    while i < len(lines):
        s = lines[i].strip()

        if lines[i].startswith("[") and s.endswith("]"):
            if id:
                data = collapse_line_continuation(data)
                data = strip_list(data)
                ret.append(TestItem(id, arg, data, i0 + 1, i))

            i0 = i
            id = s[1:-1]
            arg = None
            if " " in id:
                arg = id[id.index(" ") + 1 :]
                id = id[: id.index(" ")]
            data = []
        elif lines[i].startswith("\\["):
            data.append(lines[i][1:])
        elif not lines[i].startswith("--"):
            data.append(lines[i])
        elif lines[i].startswith("----"):
            data.append(lines[i][2:])
        i += 1

    # Process the last item.
    if id:
        data = collapse_line_continuation(data)
        data = strip_list(data)
        ret.append(TestItem(id, arg, data, i0 + 1, i - 1))

    return ret

