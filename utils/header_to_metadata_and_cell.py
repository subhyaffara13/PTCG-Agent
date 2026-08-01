
def header_to_metadata_and_cell(lines, header_prefix, header_suffix, ext=None, root_level_metadata_as_raw_cell=True):
    """
    Return the metadata, a boolean to indicate if a jupyter section was found,
    the first cell of notebook if some metadata is found outside
    the jupyter section, and next loc in text
    """

    header = []
    jupyter = []
    in_jupyter = False
    in_html_div = False

    start = 0
    started = False
    ended = False
    metadata = {}
    i = -1

    comment = "#" if header_prefix == "#'" else header_prefix

    encoding_re = re.compile(rf"^[ \t\f]*{re.escape(comment)}.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")

    for i, line in enumerate(lines):
        if i == 0 and line.startswith("#!"):
            metadata.setdefault("jupytext", {})["executable"] = line[2:]
            start = i + 1
            continue
        if i == 0 or (i == 1 and not encoding_re.match(lines[0])):
            encoding = encoding_re.match(line)
            if encoding:
                if encoding.group(1) != "utf-8":
                    raise ValueError("Encodings other than utf-8 are not supported")
                metadata.setdefault("jupytext", {})["encoding"] = line
                start = i + 1
                continue
        if not line.startswith(header_prefix):
            break
        if not comment:
            if line.strip().startswith("<!--"):
                in_html_div = True
                continue

        if in_html_div:
            if ended:
                if "-->" in line:
                    break
            if not started and not line.strip():
                continue

        line = uncomment_line(line, header_prefix, header_suffix)
        if _HEADER_RE.match(line):
            if not started:
                started = True
                continue
            ended = True
            if in_html_div:
                continue
            break

        # Stop if there is something else than a YAML header
        if not started and line.strip():
            break

        if _JUPYTER_RE.match(line):
            in_jupyter = True
        elif line and not _LEFTSPACE_RE.match(line):
            in_jupyter = False

        if in_jupyter:
            jupyter.append(line)
        else:
            header.append(line)

    if ended:
        if jupyter:
            extra_metadata = metadata
            metadata = yaml.safe_load("\n".join(jupyter))["jupyter"]
            recursive_update(metadata, extra_metadata)

        lines_to_next_cell = 1
        if len(lines) > i + 1:
            line = uncomment_line(lines[i + 1], header_prefix)
            if not _BLANK_RE.match(line):
                lines_to_next_cell = 0
            else:
                i = i + 1
        else:
            lines_to_next_cell = 0

        if header:
            if root_level_metadata_as_raw_cell:
                cell = new_raw_cell(
                    source="\n".join(["---"] + header + ["---"]),
                    metadata=(
                        {}
                        if lines_to_next_cell == pep8_lines_between_cells(["---"], lines[i + 1 :], ext)
                        else {"lines_to_next_cell": lines_to_next_cell}
                    ),
                )
            else:
                cell = None
                root_level_metadata = yaml.safe_load("\n".join(header))
                metadata.setdefault("jupytext", {})["root_level_metadata"] = root_level_metadata
        else:
            cell = None

        return metadata, jupyter, cell, i + 1

    return metadata, False, None, start

