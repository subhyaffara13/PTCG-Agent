import os
from pathlib import Path


def metadata_save(local_path: str | Path, data: dict) -> None:
    """
    Save the metadata dict in the upper YAML part Trying to preserve newlines as
    in the existing file. Docs about open() with newline="" parameter:
    https://docs.python.org/3/library/functions.html?highlight=open#open Does
    not work with "^M" linebreaks, which are replaced by \n
    """
    line_break = "\n"
    content = ""
    # try to detect existing newline character
    if os.path.exists(local_path):
        with open(local_path, newline="", encoding="utf8") as readme:
            content = readme.read()
            if isinstance(readme.newlines, tuple):
                line_break = readme.newlines[0]
            elif isinstance(readme.newlines, str):
                line_break = readme.newlines

    # creates a new file if it not
    with open(local_path, "w", newline="", encoding="utf8") as readme:
        data_yaml = yaml_dump(data, sort_keys=False, line_break=line_break)
        # sort_keys: keep dict order
        match = REGEX_YAML_BLOCK.search(content)
        if match:
            output = content[: match.start()] + f"---{line_break}{data_yaml}---{line_break}" + content[match.end() :]
        else:
            output = f"---{line_break}{data_yaml}---{line_break}{content}"

        readme.write(output)
        readme.close()

