from pathlib import Path


def _embed_headers(
    content: list[str], include_dirs: list[Path], processed_files: set[str]
) -> str:
    for line_idx, cur_line in enumerate(content):
        # Eliminate warning: `#pragma once in main file`
        if cur_line.startswith("#pragma once"):
            content[line_idx] = ""
            continue
        m = _match('^\\s*#include\\s*[<"]([^>"]+)[>"]', cur_line)
        if m is None:
            continue
        for include_dir in include_dirs:
            path = include_dir / m[1]
            if not path.exists():
                continue
            if str(path) in processed_files:
                content[line_idx] = ""
                continue
            processed_files.add(str(path))
            content[line_idx] = _embed_headers(
                read_file(path), include_dirs, processed_files
            )
            break
    return "".join(content)

